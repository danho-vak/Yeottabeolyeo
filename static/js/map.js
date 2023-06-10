var getPinDebounceTimer = null;  // getPin debounce timer

var map;  // 지도 instance
var currentPosition = [953893, 1952017]; // 기본값: 서울시청;
var currentCenterMarker;  // 나의 위치 Marker
var pinPopover;  // pin popover

// 현재 위치로 지도 영역 이동
const moveToCurrentLocation = () => {
  if (!navigator.geolocation) map.setView(sop.utmk(953893, 1952017), 12);  // 기본값: 서울시청;

  navigator.geolocation.getCurrentPosition((position) => {
    const utmkXY = new sop.LatLng (position.coords.latitude, position.coords.longitude);
    map.setView(sop.utmk(utmkXY.x, utmkXY.y), 12);
    currentPosition = [utmkXY.x, utmkXY.y];
  });
}

// 현재 위치 Marker 추가
const addCurrentPositionMarker = () => {
  if (currentCenterMarker) currentCenterMarker.remove();
  const currentCenter = map.getCenter();

  currentCenterMarker = sop.marker([currentCenter.x, currentCenter.y], {
    icon: sop.icon({iconUrl: USER_PIN_IMAGE_PATH})  // marker image 변경
  });
  currentCenterMarker.addTo(map);
}

// 지도 영역 내 수거함 pin 모두 제거
const clearBoxPin = () => {
  map.eachLayer((layer) => {
    if (layer.options.icon && layer.options.icon.options.isBoxPin) {
      layer.remove();
    }
  });
}

// 지도 영역 내 수거함 pin 추가
const getPin = (type) => {
  // 화면 x, y 좌표 구하기
  const bounds = map.getBounds();
  const swLatLng = bounds.getSouthWest();
  const neLatLng = bounds.getNorthEast();

  // x 좌표 시작 - 끝
  const xStart = swLatLng.x;
  const xEnd = neLatLng.x;

  // y 좌표 시작 - 끝
  const yStart = swLatLng.y;
  const yEnd = neLatLng.y;

  // 요청 파라미터 설정
  const csrftoken = getCookie('csrftoken');
  const url = GET_PIN_URL;
  let queryString = `?xStart=${xStart}&xEnd=${xEnd}&yStart=${yStart}&yEnd=${yEnd}`;
  if (type) {  // 특정 타입만 포함 여부
    queryString += `&type=${type}`;
  }

  const headers = {
    'X-CSRFToken': csrftoken,
    'Content-Type': 'application/json',
  };
  const options = {
    method: 'GET',
    headers: headers,
  };
  fetch(url + queryString, options)
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('Error: pin 정보 요청 실패');
      }
    }).then((result) => {
      // pin 없으면 종료
      if (Object.keys(result.data).length <= 0) return;

      // pin 추가
      result.data.forEach((item) => {
        // type에 따른 image 변경
        let pinImageUrl = CB_PIN_IMAGE_PATH;
        if (item.type === 'B') {
          pinImageUrl = BL_PIN_IMAGE_PATH;
        }

        // marker object 생성
        const pin = sop.marker([item.x, item.y], {
          icon: sop.icon({
            iconUrl: pinImageUrl,  // marker image 변경
            isBoxPin: true,  // box pin 여부
          }),
        })
        // marker click event 바인딩
        pin.on('click', (ev) => {
          const type = `${item.type === 'C' ? '의류수거함' : '폐건전지수거함'}`;
          const address = item.lot_address || item.load_address;
          const content = `${type} - ${address}`;
          ev.target.bindInfoWindow(content).openInfoWindow();
        });
        pin.addTo(map);
      });
    });
};

// 기본 컨트롤 버튼 영역 하단에 버튼 elem을 추가하는 함수
const addButton = (map, btnElem) => {
  // 기본 컨트롤 버튼 영역 하단에 위치함
  const setUI = sop.control({position :'topright'});

  // 커스텀 버튼 wrapper 생성
  setUI.onAdd = function (_map) {
    this._div = sop.DomUtil.create('div', 'custom-button-area');
    sop.DomEvent.disableClickPropagation(this._div);
    this.update();
    $(this._div).attr("id", 'set_map');
    return this._div;
  }

  // 생성된 영역에 버튼 elem을 추가
  setUI.update = function (_props) {
    this._div.append(btnElem);
  }

  // map에 추가
  setUI.addTo(map);
}

// 버튼 Elem 생성
const buildBtnElem = (btnImageUrl, clickHandler) => {
  const btnElem = document.createElement('div');
  const btnImg = document.createElement('img');
  btnImg.src = btnImageUrl;

  // 버튼 Elem 설정
  btnElem.role = 'button';
  btnElem.append(btnImg);
  btnElem.addEventListener('click', clickHandler);

  // 버튼 Elem 반환
  return btnElem;
}

const getAllTypeBoxButton = () => {
  return buildBtnElem(ALL_BTN_IMAGE_PATH, () => {
    clearBoxPin();
    // 비동기 요청 debounce
    if (getPinDebounceTimer) clearTimeout(getPinDebounceTimer);
    getPinDebounceTimer = setTimeout(() => {
      getPin();
    }, 500); // 0.5초
  });
}

// 의류 수거함 버튼 Elem 생성
const getTypeCBoxButton = () => {
  return buildBtnElem(CB_BTN_IMAGE_PATH, () => {
    clearBoxPin();
    // 비동기 요청 debounce
    if (getPinDebounceTimer) clearTimeout(getPinDebounceTimer);
    getPinDebounceTimer = setTimeout(() => {
      getPin('C');
    }, 500); // 0.5초
  });
}

// 폐건전지수거함 버튼 Elem 생성
const getTypeBBoxButton = () => {
  return buildBtnElem(BL_BTN_IMAGE_PATH, () => {
    clearBoxPin();
    // 비동기 요청 debounce
    if (getPinDebounceTimer) clearTimeout(getPinDebounceTimer);
    getPinDebounceTimer = setTimeout(() => {
      getPin('B');
    }, 500); // 0.5초
  });
}

// 현재 위치로- 버튼 Elem 생성
const getWhereAmIButton = () => {
  return buildBtnElem(WHERE_AM_I_IMAGE_PATH, () => moveToCurrentLocation());
}

// 지도 영역 내 수거함 pin 추가 debounce
const renderMap = () => {
  // 지도 instance 생성
  map = sop.map("map", {
    measureControl: false,  // 측량 관련 버튼 비활성화
    attributionControl: true,
  });

  map.zoomControl.remove();  // zoom 버튼 제거

  // 지도에 커스텀 버튼 추가
  [
    getAllTypeBoxButton(), // 전체 Type
    getTypeCBoxButton(),  // C Type
    getTypeBBoxButton(),  // B Type
    getWhereAmIButton(),  // 현재 위치로 이동
  ].forEach((btnElem) => {
    addButton(map, btnElem);
  });

  // 화면 중앙 이동 및 현재 위치 Marker 추가
  new Promise((resolve) => {
    moveToCurrentLocation();  // 현재 위치로 지도 영역 이동
    setInterval(() => resolve(), 200);
  }).then(() => {
    addCurrentPositionMarker();  // 현재 위치 Marker 추가
  });

  // 지도 이동 시작 event listener
  map.addEventListener('movestart', (event) => {
    clearBoxPin();  // 기존 pin 제거
  });

  // 지도 이동 종료 event listener
  map.addEventListener('moveend', (event) => {
    // 비동기 요청 debounce
    if (getPinDebounceTimer) clearTimeout(getPinDebounceTimer);
    getPinDebounceTimer = setTimeout(() => {
      getPin();
    }, 500); // 0.5초
  });
};

document.addEventListener('DOMContentLoaded', function() {
  renderMap();
});
