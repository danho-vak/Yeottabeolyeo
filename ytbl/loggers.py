import logging


class DisallowedHostLogHandler(logging.StreamHandler):
    """
    DisallowedHost Exception 발생시 메일 발송하는 AdminEmailHandler(logging.handler)를 호출해 console, email 로깅을 수행한다.
    이 커스텀 로그 핸들러는 위 기능에서 email 전송을 제외한, console stdout write만을 수행한다.
    """

    def get_client_ip(self, request):
        """
        request 정보에서 ip 추출
        """

        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def emit(self, record):
        """
        record(LogRecord) object는 기본적으로 request를 포함하지 않으나,
        로거 클래스 django.security.DisallowedHost는 record에 request를 포함해줌
        """

        message_format = "Invalid HTTP_HOST header (Disallowed Host)"

        request = record.request
        ip = self.get_client_ip(request)

        record.ip = ip
        record.request_method = request.method
        record.msg = message_format.format(ip=ip)
        super().emit(record)
