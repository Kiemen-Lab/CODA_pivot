// NOTE: Requires QuPath 0.6+

// USAGE
// Create a QuPath project and import all image files you'd like to downsample, then run script.
// Select the desired maximum resolution in pixels.
// For images with multiple Z-slices, timepoints, or channels, select the desired
//    Z-slice, timepoint, or channel(s).
//    Only select exactly 1 or 3 channels.
// Downsampled .tif images will be located in [PROJECT_BASE_DIR]/export

import qupath.lib.images.ImageData
import qupath.lib.objects.PathObjects
import qupath.lib.roi.ROIs
import qupath.lib.scripting.QP
import qupath.lib.regions.ImagePlane
import qupath.fx.dialogs.Dialogs
import qupath.lib.regions.RegionRequest
import qupath.lib.common.GeneralTools
import qupath.lib.images.servers.TransformedServerBuilder
import javax.swing.*
import java.awt.*
import qupath.lib.gui.tools.GuiTools
import java.awt.image.BufferedImage

// Get the current project
def project = QP.getProject()
if (!project) {
    Dialogs.showErrorMessage("No project selected", "Open a project first!")
    return
}

// Prompt user for maximum dimension
def maxDimension = Dialogs.showInputDialog("Set Maximum Dimension", "Enter the maximum dimension (in pixels):", "2000").toInteger()

// Process each image in the project
project.getImageList().each { entry ->
    // Read image data
    def imageData = entry.readImageData()
    def server = imageData.getServer()
    def metadata = server.getMetadata()
    
    // Determine Z, T, and C dimension size
    int sizeZ = metadata.getSizeZ()
    int sizeT = metadata.getSizeT()
    int sizeC = metadata.getSizeC()
    
    // Initialize variables for Z, T, and C choices
    int z = 0
    int t = 0
    int c = 0
    String channelName = null
    
    // Prompt for Z if multiple slices
    if (sizeZ > 1) {
        def zOptions = (0..<sizeZ).collect { "Z $it" }
        def zChoice = Dialogs.showChoiceDialog("Z Selection", "Select Z slice for ${entry.getImageName()}", zOptions, zOptions[0])
        z = zOptions.indexOf(zChoice)
    }
    
    // Prompt for T if multiple time points
    if (sizeT > 1) {
        def tOptions = (0..<sizeT).collect { "T $it" }
        def tChoice = Dialogs.showChoiceDialog("Time Selection", "Select time point for ${entry.getImageName()}", tOptions, tOptions[0])
        t = tOptions.indexOf(tChoice)
    }
    
    // Select channels automatically if exactly 3 exist, otherwise prompt
    def selectedChannels = []
    def channelNames = (0..<sizeC).collect { i ->
        def name = metadata.getChannels()?.get(i)?.getName()
        return (name ?: "Channel ${i}") as String
    }
    
    if (sizeC == 3) {
        selectedChannels = [0, 1, 2]
        println "Image ${entry.getImageName()} is already a 3 channel RGB image"
    } else if (sizeC > 1) {
        // Create channel select dialog
        def panel = new JPanel(new BorderLayout())
        def list = new JList(channelNames as String[])
        list.selectionMode = ListSelectionModel.MULTIPLE_INTERVAL_SELECTION
        panel.add(new JScrollPane(list), BorderLayout.CENTER)
    
        def result = JOptionPane.showConfirmDialog(
            null, panel, "Select exactly 1 or 3 channels for ${entry.getImageName()}",
            JOptionPane.OK_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE
        )
    
        if (result == JOptionPane.OK_OPTION) {
            selectedChannels = list.selectedIndices.toList()*.intValue()
        }
    }
    
    // If no channels selected, use first 3 channels
    if (selectedChannels.isEmpty()) {
        selectedChannels = [0]
    }
    
    // Ensure we have exactly 3 channels by duplicating the first if needed
    while (selectedChannels.size() < 3) {
        selectedChannels.add(selectedChannels[0])
    }
    
    // Attempt to place DAPI/NUCLEAR as blue (last) channel
    if (selectedChannels.size() == 3) {
        def dapiIndex = selectedChannels.find { i ->
            channelNames[i].toUpperCase().contains("DAPI") || channelNames[i].toUpperCase().contains("NUC")
        }
    
        if (dapiIndex != null && selectedChannels.indexOf(dapiIndex) != 2) {
            // Move DAPI/NUCLEAR channel to end (blue)
            selectedChannels.removeElement(dapiIndex)
            selectedChannels.add(dapiIndex)
            println "Reordered channels so '${channelNames[dapiIndex]}' is used as blue (channel 2)"
        }
    }
    
    // Create plane using desired C, Z, and T
    int firstC = selectedChannels[0]
    def plane = ImagePlane.getPlaneWithChannel(firstC, z, t)
    
    // Select entire image with rectangular annotation in the chosen plane
    def roi = ROIs.createRectangleROI(
        0, 
        0, 
        server.getWidth(), 
        server.getHeight(), 
        plane
    )
    def annotation = PathObjects.createAnnotationObject(roi)
    
    // Clear existing objects and add annotation
    imageData.getHierarchy().clearAll()
    imageData.getHierarchy().addObject(annotation)
    
    // Save the annotation to the project
    entry.saveImageData(imageData)
    
    // Prepare export parameters
    def rawName = new File(server.getPath()).getName()
    def cleanName = rawName.replaceAll(/\[.*?\]/, "")  // removes [--series, 0] or similar
    def name = GeneralTools.stripExtension(cleanName)
    def pathOutput = buildFilePath(PROJECT_BASE_DIR, 'export')
    mkdirs(pathOutput)
    
    // Calculate downsample factor
    def width = server.getWidth()
    def height = server.getHeight()
    
    double downsample = 1.0
    if (Math.max(width, height) > maxDimension) {
        downsample = Math.max(width, height) / maxDimension
        println "Downsampling ${entry.getImageName()} by factor ${downsample}"
    } else {
        println "Image ${entry.getImageName()} is smaller than max dimension; skipping scaling."
    }
    
    // Build server with selected channels
    int[] channelsArray = selectedChannels*.intValue() as int[]
    def multiChannelServer = new TransformedServerBuilder(server)
        .extractChannels(channelsArray)
        .build()
        
    // multiChannelServer = new qupath.lib.images.servers.TypeConvertImageServer(multiChannelServer, PixelType.UINT8)
    
    // Export the region for the annotation
    imageData.getHierarchy().getAnnotationObjects().each { ann ->
        def region = RegionRequest.createInstance(
            multiChannelServer.getPath(), 
            downsample, 
            ann.getROI()
        )
        def outputPath = buildFilePath(pathOutput, name + ".tif")
        def img = multiChannelServer.readRegion(region)

        def raster = img.getRaster()
        def widthImg = img.getWidth()
        def heightImg = img.getHeight()
        def bands = raster.getNumBands()

        def rgbImg = new BufferedImage(widthImg, heightImg, BufferedImage.TYPE_INT_RGB)

        // Calculate the per-channel min and max
        def minVals = new double[bands]
        def maxVals = new double[bands]
        Arrays.fill(minVals, Double.MAX_VALUE)
        Arrays.fill(maxVals, -Double.MAX_VALUE)
        
        // Compute per-channel min and max
        for (int y = 0; y < heightImg; y++) {
            for (int x = 0; x < widthImg; x++) {
                for (int b = 0; b < bands; b++) {
                    double v = raster.getSampleDouble(x, y, b)
                    if (v < minVals[b]) minVals[b] = v
                    if (v > maxVals[b]) maxVals[b] = v
                }
            }
        }
        def ranges = (0..<bands).collect { i ->
            def r = maxVals[i] - minVals[i]
            return (r == 0) ? 1.0 : r
        }

        // Write normalized RGB image
        for (int y = 0; y < heightImg; y++) {
            for (int x = 0; x < widthImg; x++) {
                int r = 0, g = 0, b = 0

                r = ((raster.getSampleDouble(x, y, 0) - minVals[0]) / ranges[0] * 255.0) as int
                g = ((raster.getSampleDouble(x, y, Math.min(1, bands - 1)) - minVals[Math.min(1, bands - 1)]) / ranges[Math.min(1, bands - 1)] * 255.0) as int
                b = ((raster.getSampleDouble(x, y, Math.min(2, bands - 1)) - minVals[Math.min(2, bands - 1)]) / ranges[Math.min(2, bands - 1)] * 255.0) as int
                
                r = Math.min(255, Math.max(0, r))
                g = Math.min(255, Math.max(0, g))
                b = Math.min(255, Math.max(0, b))

                int rgb = (r << 16) | (g << 8) | b
                rgbImg.setRGB(x, y, rgb)
            }
        }

        writeImage(rgbImg, outputPath)

    }
    
    // Save downsample factor and RGB channel names to a .csv file
    def csvLines = []
    downsample = 1 / downsample
    csvLines << "DownsampleFactor"
    csvLines << "${downsample}"
    csvLines << ""
    csvLines << "RGB_Channel_Mapping"
    if (selectedChannels.size() == 3) {
        csvLines << "Red,${channelNames[selectedChannels[0]]}"
        csvLines << "Green,${channelNames[selectedChannels[1]]}"
        csvLines << "Blue,${channelNames[selectedChannels[2]]}"
    } else if (selectedChannels.size() == 1) {
        csvLines << "Grayscale,${channelNames[selectedChannels[0]]}"
    }
    
    def csvPath = buildFilePath(pathOutput, name + ".csv")
    new File(csvPath).text = csvLines.join("\n")
    
    println "Processed: ${entry.getImageName()}"
}

Dialogs.showInfoNotification("Complete", "Processed ${project.size()} images")