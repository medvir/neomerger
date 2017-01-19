# Convert the ico image to icns for Mac

    sips -s format tiff dlicon.ico --out dlicon.tiff
    tiff2icns -noLarge dlicon.tiff dlicon.icns
