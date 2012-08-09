from twisted.web import server, resource
from twisted.internet import reactor
from twisted.web.static import File
from consecutive import consecutive

def dummy(request):
	return "{}"


graphfunctions = {'consecutive' : consecutive}

class JSON(resource.Resource):
    isLeaf = True
	
    def render_GET(self, request):
        if request.args and request.path.endswith(".json"):
            try:
                functionname = request.args["function"][0]
                print repr(functionname), graphfunctions
                function = graphfunctions[functionname]
                print function

                return "some output" + function(request.args)
            
            except KeyError as error: return "Unrecognised function", error
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
try:
    reactor.run()
except:
    reactor.stop()

