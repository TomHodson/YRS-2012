from twisted.web import server, resource
from twisted.internet import reactor
from twisted.web.static import File
from consecutive import consecutive

def dummy(request):
    return "{}"


graphfunctions = {'dummy' : dummy}

class JSON(resource.Resource):
    isLeaf = True
	
    def render_GET(self, request):
        if request.args and request.path.endswith(".json"):
            seed = request.args['word'][0]
            depth = request.args['depth'][0]
            #HANDLE json REQUESTS HERE
            return ""
        else:
            request.setHeader("content-type", "text/html")
            if request.path == '/':
                return open('./mainpage.html').read()
            else:
                try:    	
                    return open('.{path}'.format(path=request.path)).read()
                except IOError:
                    request.setResponseCode(404)
                    return 'Error'
   	


reactor.listenTCP(8000, server.Site(JSON()))
reactor.run()
