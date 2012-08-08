from twisted.web import server, resource
from twisted.internet import reactor
from twisted.web.static import File
from consecutive import consecutive

def dummy(request):
    return "{}"


graphfunctions = {'dummy' : dummy}

class JSON(resource.Resource):
<<<<<<< HEAD
	isLeaf = True
	
	def render_GET(self, request):
		print 'a get request'
		
		if not request.args: # if there are no args
			request.setHeader("content-type", "text/html")
			if request.path == '/':
				return open('./index.html').read()
			else:
				try:	
					return open('.{path}'.format(path=request.path)).read()
				except IOError:
					request.setResponseCode(404)
					return 'Error'
=======
    isLeaf = True
    
    def render_GET(self, request):
        print 'a get request'
    	
        if not request.args: # if there are no args
            request.setHeader("content-type", "text/html")
            return open('mainpage.html').read()
>>>>>>> 5aa2f50c757ea1b8f0bbd134fd97ddf93497ce9a


        else:
            request.setHeader("content-type", "application/json")

            #function = graphfunctions[request.args['graphtype']]
            if request.args['graphtype'][0] == "consec":
                return "consec"
            return function(request)
   	


reactor.listenTCP(8000, server.Site(JSON()))
reactor.run()
