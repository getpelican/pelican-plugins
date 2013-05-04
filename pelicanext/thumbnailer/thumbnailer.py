import os
from PIL import Image
from pelican import signals
from pilkit.processors import *

def thumbnailer(generator):

    resize = generator.settings['RESIZE']
    
    outputpath = generator.settings['OUTPUT_PATH']
    imagesoutputpath = os.path.join(outputpath,'static', 'images')
    
    
    for path, overwrite, suffix, processes in resize:
    
    	processor = ProcessorPipeline(processes)
    	
    	processpath = os.path.join(imagesoutputpath, path)
    	
        for dirpath, dirnames, filenames in os.walk(processpath):
            for name in filenames:
                imagepath = os.path.join(dirpath, name)
                
                #Find output path
                if overwrite:
                    outputimagepath=imagepath
                else:
                   relpath = os.path.join(os.path.relpath(dirpath,processpath), name)
                   thumbnailpath = os.path.join(imagesoutputpath, path+suffix)
                   outputimagepath = os.path.join(thumbnailpath,relpath)
                
                #Create output directory if it doesnt exist
                (dpath,dfile) = os.path.split(outputimagepath)
        	if not os.path.isdir(dpath):
        	    os.makedirs(dpath)
        	    
                #Process image                
                image = Image.open(imagepath)
                image = processor.process(image)
                
                image.save(outputimagepath)



def register():
    signals.finalized.connect(thumbnailer)
