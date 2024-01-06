from tkinter import messagebox

import cv2
from PIL import Image
import PIL.Image
import PIL.ImageChops
import PIL.ImageOps
import Global_Setting_Var

def concatenate_images_vertically(image1_path, image2_path, output_path):
    # Use the default associated program to open the file
    try:
        # Open the images
        img1 = Image.open(image1_path)
        img2 = Image.open(image2_path)

    except FileNotFoundError:
        messagebox.showinfo("Error", "the desire files weren't found .")
    except Exception as e:
        messagebox.showinfo("Error", f"An error occurred: {e}")



    # Ensure both images have the same width
    if img1.width != img2.width:
        raise ValueError("Both images must have the same width.")

    # Calculate the height of the concatenated image
    new_height = img1.height + img2.height

    # Create a new image with the same width and combined height
    new_img = Image.new('RGB', (img1.width, new_height))

    # Paste the first image at the top
    new_img.paste(img1, (0, 0))

    # Paste the second image below the first one
    new_img.paste(img2, (0, img1.height))

    # Save the result
    new_img.save(output_path)

def Create_Def_Image(FileNameSource, FileNameNew, number):
    Image1 = PIL.Image.open(FileNameSource)
    Image2 = PIL.Image.open(FileNameNew)
    diff = PIL.ImageChops.difference(Image1, Image2)

    # Apply a threshold to consider only significant differences
    diff = diff.point(lambda p: p > Global_Setting_Var.image_treshold and 255)

    DifffileNameImage =FileNameNew[:-7] + "N_Diff.jpg"
    diff.save(DifffileNameImage)

#FileNameNew, FileNameSource, path, Global_Setting_Var.image_treshold

def calcdiffrance(FileNameNew,FileNameSource,path,scale,fileNameImage_number):

    # crop the image from the current running - result one
    image_X_Size, Image_Y_Size = crop_image(FileNameNew,Global_Setting_Var.f6_TopLeft_Y, Global_Setting_Var.f6_TopLeft_X, Global_Setting_Var.f6_ButtomRight_Y, Global_Setting_Var.f6_ButtomRight_X)

    # add name for the cutting image
    FileNameNew_cut = FileNameNew[:-4] + "_cut.jpg"
    # find above 80 % correlation between the picture are - find the offset
    percentage_found, Max = find_template_percentage(FileNameNew_cut, FileNameSource,Global_Setting_Var.genaralSimilarity )

    if percentage_found == 0 : # we didnt get 80% of similarity between the picture somthing is very wrong
        Max = (0,0)

    # calculate the source image boundaries for the cut
    main_image = Image.open(FileNameSource)
    MI_BX = abs(main_image.size[0]-image_X_Size - Max[0])
    MI_BY = abs(main_image.size[1]-Image_Y_Size - Max[1])

    # crop the image from the current running - Source one
    image_X_Size2, Image_Y_Size2 = crop_image(FileNameSource, Max[1],Max[0],MI_BY, MI_BX)

    FileNameSource_cut = FileNameSource[:-4] + "_cut.jpg"


    diff = 0

    img_a_pixels_open = PIL.Image.open(FileNameSource_cut)
    img_b_pixels_open = PIL.Image.open(FileNameNew_cut)

    img_a_pixels_grey = PIL.ImageOps.grayscale(img_a_pixels_open)
    img_b_pixels_grey = PIL.ImageOps.grayscale(img_b_pixels_open)

    GreyScaleSourec = path + "\GS_Source.jpg"
    GreyScaleNew = path + "\GS_target.jpg"

    img_a_pixels_grey.save(GreyScaleSourec)
    img_b_pixels_grey.save(GreyScaleNew)

    img_a_pixels_grey_data = PIL.Image.open(GreyScaleSourec).getdata()
    img_b_pixels_grey_data = PIL.Image.open(GreyScaleNew).getdata()

    for pixel_g_a, pixel_g_b in zip(img_a_pixels_grey_data, img_b_pixels_grey_data):
        if abs(pixel_g_a - pixel_g_b) > scale:
            diff = diff + 1

    # print("Total pixels:", img_a_pixels_open.size[0] * img_a_pixels_open.size[1])
    # print("Number of differing pixels:", diff)
    Create_Def_Image(FileNameSource_cut, FileNameNew_cut,fileNameImage_number)
    return diff


def crop_image(input_path,TopY, TopX, BottomY, Bottomx):


    # Open the image
    image = Image.open(input_path)
    Max_x = image.size[0] - Bottomx
    Max_y = image.size[1] - BottomY
    # Crop the image
    cropped_image = image.crop((TopX, TopY, Max_x, Max_y))
    Targrt_path = input_path[:-4] + "_cut.jpg"
    # Save the cropped image
    cropped_image.save(Targrt_path)
    return cropped_image.size[0], cropped_image.size[1]


def find_template_percentage(template_path, search_image_path, threshold):

    # Read the template and search image
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    search_image = cv2.imread(search_image_path, cv2.IMREAD_COLOR)

    # Convert images to grayscale
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    search_image_gray = cv2.cvtColor(search_image, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(search_image_gray, template_gray, cv2.TM_CCOEFF_NORMED)

    # Find the location of the best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    #print (min_val, max_val, min_loc, max_loc)

    # Check if the maximum correlation is above the threshold
    if max_val >= float(threshold):
        # Get the dimensions of the template
        h, w = template_gray.shape

        # Calculate the percentage of the template in the search image
        template_area = w * h
        match_area = max_val * template_area

        percentage = (match_area / template_area) * 100

        # Draw a rectangle around the matched region
        #top_left = max_loc
        # bottom_right = (top_left[0] + w, top_left[1] + h)
        # cv2.rectangle(search_image, top_left, bottom_right, (0, 255, 0), 2)
        # print ("here")
        # # Display the result
        # cv2.imshow('Template Matching Result', search_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # print("here2")

        return percentage, max_loc
    else:
        # print("Template not found in the search image.")
        return 0, 0






# # Example usage
# main_image_path = "C:\projectPython\imgeprocess\S_Map_6_IOS_WEB_step_2P.jpg"
# sub_image_path = "C:\projectPython\imgeprocess\Map_6_IOS_WEB_step_2P.jpg"
# Main_image_path_cut = "C:\projectPython\imgeprocess\S_Map_6_IOS_WEB_step_22P.jpg"
# sub_image_path_cut = "C:\projectPython\imgeprocess\Map_6_IOS_WEB_step_22P.jpg"
# path ="C:\projectPython\imgeprocess"
# scale = 150

#image_X_Size, Image_Y_Size = crop_image(sub_image_path, sub_image_path_cut,100,100,100,100)

# if is_image_in_image(main_image_path, sub_image_path):
#     print("Sub-image found in the main image.")
# else:
#     print("Sub-image not found in the main image.")

    # Example usage
# percentage_found, Max= find_template_percentage(sub_image_path_cut, main_image_path)
# print(f"Percentage of template found: {percentage_found:.2f}%")
#
# diff = calcdiffrance(sub_image_path,main_image_path,path,scale)
# print(diff)
# Create_Def_Image(main_image_path, sub_image_path, 9)
#
#
# main_image = Image.open(main_image_path)
# MI_BX = abs(main_image.size[0]-image_X_Size - Max[0])
# MI_BY = abs(main_image.size[1]-Image_Y_Size - Max[1])
# image_X_Size2, Image_Y_Size2 = crop_image(main_image_path, Main_image_path_cut,Max[1],Max[0],MI_BY, MI_BX)
#
#
# diff = calcdiffrance(sub_image_path,main_image_path,path,scale)
# print(diff)
# Create_Def_Image(main_image_path, sub_image_path, 9)
#
# diff = calcdiffrance(Main_image_path_cut,sub_image_path_cut,path,scale)
# print(diff)
# Create_Def_Image(sub_image_path_cut, Main_image_path_cut, 10)
#
# print(diff)
#
