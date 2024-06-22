# PowerPoint module
import win32com.client as win32com
import shutil
import os
import requests

def open_pptx(pptx_path):
    application = win32com.Dispatch("PowerPoint.Application")
    # powerpoint.Visible = True
    presentation = application.Presentations.Open(pptx_path)
    return presentation, application

def close_pptx(presentation):
    presentation.Close()
    application = win32com.Dispatch("PowerPoint.Application")
    application.Quit()

def save_pptx(presentation, pptx_path):
    presentation.SaveAs(pptx_path)

def save_pptx_as_pdf(presentation, pdf_path):
    presentation.ExportAsFixedFormat(pdf_path, 2)

def save_pptx_as_jpeg(presentation, jpeg_path):
    presentation.ExportAsFixedFormat(jpeg_path, 17)

def save_pptx_as_png(presentation, png_path):
    presentation.ExportAsFixedFormat(png_path, 18)

def save_pptx_as_gif(presentation, gif_path):
    presentation.ExportAsFixedFormat(gif_path, 16)

def add_slide(presentation, slide_layout_index, section_index=None):
    slide_layout = presentation.SlideMaster.CustomLayouts(slide_layout_index)
    slide = presentation.Slides.AddSlide(presentation.Slides.Count + 1, slide_layout)
    if section_index is not None:
        slide.MoveToSectionStart(section_index)
    return slide

def add_title(title, presentation, slide=None, slide_index=None):
    if slide is None:
        slide = presentation.Slides(slide_index)
    slide.Shapes.Title.TextFrame.TextRange.Text = title

def add_text(text, presentation, slide=None, placeholder_index=None, slide_index=None):
    if text is None:
        return
    if slide is None:
        slide = presentation.Slides(slide_index)
    if placeholder_index is None:
        placeholder_index = 1
    slide.Shapes.Placeholders(placeholder_index).TextFrame.TextRange.Text = text

# Add a slide to a presentation
def add_slide_and_text(presentation, slide_layout_index=None, title=None, text_list=None):
    slide_layout = presentation.SlideMaster.CustomLayouts(slide_layout_index)
    slide = presentation.Slides.AddSlide(presentation.Slides.Count + 1, slide_layout)
    if title is not None:
        if slide.Shapes.Count > 0 and slide.Shapes[0].Name == 'Title 1':
            print('This is a title slide layout and a title is provided. Adding the title...')
            add_title(title, presentation, slide)
            if text_list is not None:
                print("There is also text to add")
                if isinstance(text_list, str):
                    print("It's a string!")
                    text_list = [text_list]
                    for i, text in enumerate(text_list):
                        slide.Shapes.Placeholders[i + 1].TextFrame.TextRange.Text = text
                elif isinstance(text_list, list):
                    print("It's a list! There are " + str(len(text_list)) + " items in the list.")
                    # Check if the number of items in the list is greater than the number of placeholders
                    if len(text_list) > slide.Shapes.Placeholders.Count - 1:
                        print("There are more items in the list than placeholders and we cannot proceed. Exiting...")
                        return
                    for i, text in enumerate(text_list):
                        slide.Shapes.Placeholders[i + 1].TextFrame.TextRange.Text = text
    else:
        if slide.Shapes.Count > 0 and slide.Shapes[0].Name == 'Title 1':
            print("No title provided but there is a title placeholder... This could be an error. Exiting...")
            return
        if text_list is not None:
            print("No title provided but there is text to add")
            if isinstance(text_list, str):
                print("It's a string")
                text_list = [text_list]
                for i, text in enumerate(text_list):
                    slide.Shapes.Placeholders[i].TextFrame.TextRange.Text = text
            elif isinstance(text_list, list):
                print("It's a list! There are " + str(len(text_list)) + " items in the list.")
                # Check if the number of items in the list is greater than the number of placeholders
                if len(text_list) > slide.Shapes.Placeholders.Count:
                    print("There are more items in the list than placeholders and we cannot proceed. Exiting...")
                    return
                for i, text in enumerate(text_list):
                    slide.Shapes.Placeholders[i].TextFrame.TextRange.Text = text
    return slide                

def add_section(presentation, section_index=None, section_name=None, slide_layout_index=None, title=None, text_list=None):
    slide = add_slide_and_text(presentation, slide_layout_index, title, text_list)
    print(type(slide))
    print("Adding section...")
    if section_name is None:
        if section_index is None:
            section_index = presentation.SectionProperties.Count + 1
            section_name = "Section " + str(section_index)
        else:
            section_name = "Section " + str(section_index)
    presentation.SectionProperties.AddSection(section_index, section_name)
    print("Added " + section_name + " at index " + str(section_index))
    slide.MoveToSectionStart(section_index)
    return slide

def add_image(image_path, presentation, slide=None, placeholder_index=None, slide_index=None):
    image_path = image_path.replace("/", "\\")
    if slide is None:
        slide = presentation.Slides(slide_index)
    # Check if the image exists and if not return an empty string
    if not os.path.exists(image_path):
        print("Image does not exist: " + image_path)
        return ""
    slide_width = slide.Master.Width
    slide_height = slide.Master.Height
    print("Slide width: " + str(slide_width) + ", slide height: " + str(slide_height))
    print("Adding image to slide... " + image_path + " will be added as " + image_path.replace("/", "\\"))
    total_shapes = slide.Shapes.Count
    print("Total shapes before adding image: " + str(total_shapes))
    slide.Shapes.AddPicture(image_path, LinkToFile=0, SaveWithDocument=1, Left=0, Top=0, Width=slide_width, Height=slide_height)
    total_shapes = slide.Shapes.Count
    print("Total shapes after adding image: " + str(total_shapes))
    print("Setting image to be behind all other shapes")
    slide.Shapes(total_shapes).ZOrder(1)    

# List the slide layouts in a presentation and return a dictionary of slide layout names and indices
def list_slide_layouts(presentation):
    for i in range(1, presentation.SlideMaster.CustomLayouts.Count + 1):
        slide_layout = presentation.SlideMaster.CustomLayouts.Item(i)
        print(i, slide_layout.Name)
        slide_layout_dict = {
            i: slide_layout.Name
        }
    return slide_layout_dict

# List the slide layout placeholders in an individual slide layout and return a dictionary of placeholder names and indices
def list_slide_layout_placeholders(presentation, slide_layout_index):
    # append the placeholder name and index to a dictionary
    placeholder_dict = []
    for i, placeholder in range(1, presentation.SlideMaster.CustomLayouts.Item(slide_layout_index).Shapes.Placeholders.Count + 1):
        placeholder_dict.append({
            'index': i,
            'name': placeholder.Name
        })
    return placeholder_dict

# List the placeholders in a slide
def list_slide_placeholders(presentation, slide_index):
    for i in range(1, presentation.Slides(slide_index).Shapes.Placeholders.Count + 1):
        placeholder = presentation.Slides(slide_index).Shapes.Placeholders.Item(i)
        print(i, placeholder.Name)

def pptx_to_dict(presentation):
    slide_list = []
    for slide in presentation.Slides:
        for shape in slide.Shapes:
            slide_dict = {
                'SlideNumber': slide.SlideNumber,
                'ShapeName': shape.Name,
                'TextContent': shape.TextFrame.TextRange.Text
            }
            slide_list.append(slide_dict)
            print("Slide " + str(slide.SlideNumber) + " has shape " + str(shape.Name) + " with contents " + str(shape.TextFrame.TextRange.Text))
    return slide_list
