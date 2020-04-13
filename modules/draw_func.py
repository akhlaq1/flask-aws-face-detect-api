from PIL import Image, ImageDraw, ExifTags, ImageColor    

def draw_boxes(response,stream,img_output_path):
    
    image=Image.open(stream)

    imgWidth, imgHeight = image.size  
    draw = ImageDraw.Draw(image)  
                    

    # calculate and display bounding boxes for each detected face       
    
    for faceDetail in response['FaceDetails']:
        
        box = faceDetail['BoundingBox']
        left = imgWidth * box['Left']
        top = imgHeight * box['Top']
        width = imgWidth * box['Width']
        height = imgHeight * box['Height']
                

        # print('Left: ' + '{0:.0f}'.format(left))
        # print('Top: ' + '{0:.0f}'.format(top))
        # print('Face Width: ' + "{0:.0f}".format(width))
        # print('Face Height: ' + "{0:.0f}".format(height))

        points = (
            (left,top),
            (left + width, top),
            (left + width, top + height),
            (left , top + height),
            (left, top)

        )

        draw.line(points, fill='#00d400', width=2)

        # for dots 
        dots_arr = []
        dots = faceDetail['Landmarks']
        for dot in dots:
            dots_arr.append((imgWidth * dot['X'],imgHeight *dot['Y']))
        # print(dots_arr)
        draw.point(dots_arr, fill=(255, 255, 255))


        # Alternatively can draw rectangle. However you can't set line width.
        #draw.rectangle([left,top, left + width, top + height], outline='#00d400') 

    image.save(img_output_path)
