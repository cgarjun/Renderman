#!/usr/bin/python
# for bash we need to add the following to our .bashrc
# export PYTHONPATH=$PYTHONPATH:$RMANTREE/bin   
import getpass
import time,random
# import the python renderman library
import prman



def Scene(ri) :
	ri.AttributeBegin()
	random.seed(25)
	ri.Color([0.27,0.04,0.36])
	ri.Surface(  "Velvet" ,{"float Ka": [0.050],"float Kd": [0.100],"float Ks": [0.100],"float backscatter": [0.550],"float edginess": [3.000], "color sheen": [0.275 ,0.035, 0.357], "float roughness": [0.450], })
	face=[-0.1,-1,-3, 0.1,-1,-3,-0.1,-1,3, 0.1,-1,3]
	plank=-5.0
	while (plank <=5.0) :
		ri.TransformBegin()
		c0=[random.uniform(-10,10),random.uniform(-10,10),random.uniform(-10,10)]
		c1=[random.uniform(-10,10),random.uniform(-10,10),random.uniform(-10,10)]
		
		ri.Translate(plank,0,0)
		ri.Patch("bilinear",{'P':face})
		ri.TransformEnd()
		plank=plank+0.206
	ri.AttributeEnd()
	ri.TransformBegin()
	ri.AttributeBegin()
	ri.Translate( 0,-1.0,0)
	ri.Rotate(-90,1,0,0)
	ri.Rotate(36,0,0,1)
	ri.Scale(0.4,0.4,0.4)
	ri.Color([0.27,0.04,0.36])
	ri.Surface(  "Velvet" ,{"float Ka": [0.050],"float Kd": [0.100],"float Ks": [0.100],"float backscatter": [0.550],"float edginess": [3.000], "color sheen": [0.275 ,0.035, 0.357], "float roughness": [0.450], })
	ri.Geometry("teapot")
	ri.AttributeEnd()
	ri.TransformEnd()
	
ri = prman.Ri() # create an instance of the RenderMan interface
ri.Option("rib", {"string asciistyle": "indented"})

filename = "ShaderTest.rib"
# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin("__render")
# ArchiveRecord is used to add elements to the rib stream in this case comments
# note the function is overloaded so we can concatinate output
ri.ArchiveRecord(ri.COMMENT, 'File ' +filename)
ri.ArchiveRecord(ri.COMMENT, "Created by " + getpass.getuser())
ri.ArchiveRecord(ri.COMMENT, "Creation Date: " +time.ctime(time.time()))
ri.Declare("Light1" ,"string")
ri.Declare("Light2" ,"string")
ri.Declare("Light3" ,"string")

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("ShaderTest.exr", "framebuffer", "rgba")
# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720,575,1)
# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:50}) 



# now we start our world
ri.WorldBegin()


ri.LightSource( "pointlight", {ri.HANDLEID:"Light1", "point to":[0,0,-5], "float intensity": [12]})
ri.LightSource( "spotlight", {ri.HANDLEID:"Light2", "point from":[-2,3,-5],"point to":[0,0,0], "float intensity": [3]})
ri.LightSource("ambientlight",{ri.HANDLEID: "Light3","float intensity": [0.05]})
ri.Illuminate("Light1",1)
ri.Illuminate("Light2",1)
ri.Illuminate("Light3",1)



ri.Translate(0,0,4)
Scene(ri)


ri.WorldEnd()
# and finally end the rib file
ri.End()
