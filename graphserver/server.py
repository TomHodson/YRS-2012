from twisted.web import server, resource
from twisted.internet import reactor
from twisted.web.static import File
from consecutive import consecutive

def dummy(request):
	return "{}"


graphfunctions = {'consec' : consecutive}

class JSON(resource.Resource):
	isLeaf = True
	
	def render_GET(self, request):
		print 'a get request'

		if request.args and request.path.endswith('.json'): #requesting dynamic json content

			request.setHeader("content-type", "application/json")

			function = graphfunctions[request.args['graphtype']]

			return function(request.args)
	
		else: # server static
			request.setHeader("content-type", "text/html")
			if request.path == '/':
				return open('./index.html').read()
			else:
				try:	
					return open('.{path}'.format(path=request.path)).read()
				except IOError:
					request.setResponseCode(404)
					return 'Error'

reactor.listenTCP(8000, server.Site(JSON()))
reactor.run()
