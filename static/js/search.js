const search = () => {
  const isRoadAddress = (address) => {
    const regex = /(([가-힣A-Za-z·\d~\-\.]{2,}(로|길).[\d]+))/;
    return regex.test(address);
  }

  const isLotAddress = (address) => {
    const regex = /(([가-힣A-Za-z·\d~\-\.]+(읍|동)\s)[\d-]+)|(([가-힣A-Za-z·\d~\-\.]+(읍|동)\s)[\d][^시]+)/;
    return regex.test(address);
  }

  const isDistrict = (address) => {
    const regex = /(.+구$)/;
    return regex.test(address);
  }

  // 입력값
  const inputValue = document.getElementById('search-input').value;

  // request 정보
  const url = 'https://api.vworld.kr/req/search';
  const queryParams = new URLSearchParams({
    key: VWORKD_KEY,
    request: 'search',
    query: inputValue,
  })

  // 입력값에 따른 응답 Type 설정
  let type;
  let category;
  if (isRoadAddress(inputValue)) {
    type = 'ADDRESS';
    category = 'ROAD';
  } else if (isLotAddress(inputValue)) {
    type = 'ADDRESS';
    category = 'PARCEL';
  } else if (isDistrict(inputValue)) {
    type = 'DISTRICT';
  } else {
    type = 'PLACE';
  }

  queryParams.set('type', type);
  if (category) queryParams.set('category', category);

  $.ajax({
    type: 'get',
    url: url,
    data: queryParams.toString(),
    dataType: 'jsonp',
    error: function () {
      console.log('주소 검색 API 호출 오류');
    }
  }).done((response) => {
    const data = response.response;
    if (data.status === 'OK') {
      const result = data.result.items[0];
      const utmkXY = new sop.LatLng (result.point.y, result.point.x);
      map.setView(sop.utmk(utmkXY.x, utmkXY.y), 11);
    } else if (data.status === 'NOT_FOUND') {
      alert('검색 결과가 없습니다.');
    } else {
      alert('주소 검색 중 오류가 발생했습니다.');
    }
  });
}

var searchOffCanvas;
document.addEventListener('DOMContentLoaded', () => {
  const offCanvasElem = document.getElementById('search-offcanvas');
  const searchBtnElem = document.getElementById('search-btn');
  const searchInputElem = document.getElementById('search-input');
  const searchInputBtnElem = document.getElementById('search-input-btn');

  searchOffCanvas = new bootstrap.Offcanvas(offCanvasElem);
  offCanvasElem.addEventListener('show.bs.offcanvas', () => searchBtnElem.classList.add('d-none'));
  offCanvasElem.addEventListener('shown.bs.offcanvas', () => searchInputElem.focus());
  offCanvasElem.addEventListener('hide.bs.offcanvas', () => searchBtnElem.classList.remove('d-none'));

  searchBtnElem.addEventListener('click', () => searchOffCanvas.toggle());

  searchInputElem.addEventListener('keyup', (ev) => {
    if (ev.key === 'Enter') {
      searchOffCanvas.hide();
      search();
    }
  });

  searchInputBtnElem.addEventListener('click', () => {
    searchOffCanvas.hide();
    search();
  });
});
