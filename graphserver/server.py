from twisted.web import server, resource
from twisted.internet import reactor
from twisted.web.static import File

def dummy(request):
	return "{}"


graphfunctions = {'dummy' : dummy}

class JSON(resource.Resource):
	isLeaf = True
	
	def render_GET(self, request):
		print 'a get request'
		
		if not request.args: # if there are no args
			request.setHeader("content-type", "text/html")
			return open('../ui/mainpage.html').read()


		else:
			request.setHeader("content-type", "application/json")

			function = graphfunctions[request.args['graphtype']]

			return function(request)
		


reactor.listenTCP(8000, server.Site(JSON()))
reactor.run()