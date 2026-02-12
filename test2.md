import aspose.slides as slides

with slides.Presentation("layout_source.pptx") as source_prs:
    with slides.Presentation("target.pptx") as target_prs:

        # Get the master from the source (carries all its layouts with it)
        source_master = source_prs.masters[0]

        # Clone the entire master into the target presentation
        cloned_master = target_prs.masters.add_clone(source_master)

        # Pick one of the layouts that came with the cloned master
        desired_layout = cloned_master.layout_slides[1]

        # Apply to all slides
        for slide in target_prs.slides:
            slide.layout_slide = desired_layout

        target_prs.save("result.pptx", slides.export.SaveFormat.PPTX)
