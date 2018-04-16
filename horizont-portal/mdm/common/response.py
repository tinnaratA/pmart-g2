from rest_framework.response import Response


class MdmResponse(Response):

    def __init__(self, data, status, *args, **kwargs):
        success = True if status >= 200 and status < 300 else False
        data = {"success": success, "data": data}
        super(self.__class__, self).__init__(data, status, *args, **kwargs)
