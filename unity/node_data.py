effect_node_data = {}
effect_node_data["BRIGHTCONTRAST"] = ['Birghtness / Contrast', 'CompositorNodeBrightContrast', 'IMAGE_ALPHA']
effect_node_data["VALTORGB"] = ['Color Ramp', 'CompositorNodeValToRGB', 'NODE_TEXTURE']
effect_node_data["COLORBALANCE"] = ['Color Balance', 'CompositorNodeColorBalance', 'COLOR']
effect_node_data["COLORCORRECTION"] = ['Color Correction', 'CompositorNodeColorCorrection', 'SHADERFX']
effect_node_data["EXPOSURE"] = ['Exposure', 'CompositorNodeExposure', 'SORTBYEXT']
effect_node_data["GAMMA"] = ['Gamma', 'CompositorNodeGamma', 'SEQ_HISTOGRAM']
effect_node_data["HUECORRECT"] = ['Hue Correct', 'CompositorNodeHueCorrect', 'MOD_HUE_SATURATION']
effect_node_data["HUE_SAT"] = ['HSV', 'CompositorNodeHueSat', 'MOD_HUE_SATURATION']
effect_node_data["CURVE_RGB"] = ['RGB Curve', 'CompositorNodeCurveRGB', 'NORMALIZE_FCURVES']
effect_node_data["TONEMAP"] = ['Tonemap', 'CompositorNodeTonemap', 'RIGID_BODY']
effect_node_data["INVERT"] = ['Invert Color', 'CompositorNodeInvert', 'IMAGE_RGB_ALPHA']
effect_node_data["CONVERT_COLORSPACE"] = ['Convert ColorSpace', 'CompositorNodeConvertColorSpace', 'SEQ_SPLITVIEW']
effect_node_data["SEPARATE_COLOR"] = ['Separate Color', 'CompositorNodeSeparateColor', 'PARTICLES']

effect_node_data["ANTIALIASING"] = ['Anti-Aliasing', 'CompositorNodeAntiAliasing', 'IPO_CONSTANT']
effect_node_data["DESPECKLE"] = ['Despecklet', 'CompositorNodeDespeckle', 'IPO_EASE_IN_OUT']
effect_node_data["INPAINT"] = ['InPaint', 'CompositorNodeInpaint', 'BRUSH_DATA']
effect_node_data["FILTER"] = ['Filter', 'CompositorNodeFilter', 'FILTER']
effect_node_data["GLARE"] = ['Glare', 'CompositorNodeGlare', 'SHADING_RENDERED']
effect_node_data["KUWAHARA"] = ['Kuwahara', 'CompositorNodeKuwahara', 'IMAGE_DATA']
effect_node_data["PIXELATE"] = ['Pixelate', 'CompositorNodePixelate', 'MOD_REMESH']
effect_node_data["POSTERIZE"] = ['Posterize', 'CompositorNodePosterize', 'COLORSET_10_VEC']
effect_node_data["SUNBEAMS"] = ['Sun Beams', 'CompositorNodeSunBeams', 'LIGHT_SUN']
effect_node_data["LENSDIST"] = ['Lens Distortion', 'CompositorNodeLensdist', 'RESTRICT_RENDER_OFF']

effect_node_data["BILATERALBLUR"] = ['Bilateral Blur', 'CompositorNodeBilateralblur', 'CLIPUV_HLT']
effect_node_data["BLUR"] = ['Blur', 'CompositorNodeBlur', 'CLIPUV_HLT']
effect_node_data["BOKEHBLUR"] = ['Bokeh Blur', 'CompositorNodeBokehBlur', 'CLIPUV_HLT']
effect_node_data["DEFOCUS"] = ['Defocus', 'CompositorNodeDefocus', 'CLIPUV_HLT']
effect_node_data["DBLUR"] = ['Directional Blur', 'CompositorNodeDBlur', 'CLIPUV_HLT']


effect_node_data["CRYPTOMATTE"] = ['Cryptomatte (Legacy)', 'CompositorNodeCryptomatte', 'EYEDROPPER']

effect_node_data["CHANNEL_MATTE"] = ['Channel Key', 'CompositorNodeChannelMatte', 'KEYINGSET']
effect_node_data["CHROMA_MATTE"] = ['Chroma Key', 'CompositorNodeChromaMatte', 'KEYINGSET']
effect_node_data["COLOR_MATTE"] = ['Color Key', 'CompositorNodeColorMatte', 'KEYINGSET']
effect_node_data["COLOR_SPILL"] = ['Color Spill', 'CompositorNodeColorSpill', 'KEYINGSET']
effect_node_data["DISTANCE_MATTE"] = ['Distance Key', 'CompositorNodeDistanceMatte', 'KEYINGSET']
effect_node_data["KEYING"] = ['Keying', 'CompositorNodeKeying', 'KEYINGSET']
effect_node_data["LUMA_MATTE"] = ['Luminance Key', 'CompositorNodeLumaMatte', 'KEYINGSET']

effect_node_data["TRANSFORM"] = ['Transform', 'CompositorNodeTransform', 'CON_TRANSFORM']
effect_node_data["TRANSLATE"] = ['Translate', 'CompositorNodeTranslate', 'CON_LOCLIKE']
effect_node_data["ROTATE"] = ['Rotate', 'CompositorNodeRotate', 'CON_ROTLIKE']
effect_node_data["SCALE"] = ['Scale', 'CompositorNodeScale', 'CON_SIZELIKE']

effect_node_data["CORNERPIN"] = ['Corner Pin', 'CompositorNodeCornerPin', 'PINNED']
effect_node_data["CROP"] = ['Crop', 'CompositorNodeCrop', 'AREA_DOCK']
effect_node_data["FLIP"] = ['Flip', 'CompositorNodeFlip', 'MOD_MIRROR']

source_node_data = {}
source_node_data['R_LAYERS'] = ['Render Layer', 'CompositorNodeRLayers', 'RENDER_RESULT']
source_node_data['IMAGE'] = ['Image', 'CompositorNodeImage', 'OUTLINER_OB_IMAGE']
source_node_data['MOVIECLIP'] = ['Movie', 'CompositorNodeMovieClip', 'SEQUENCE']
source_node_data['RGB'] = ['Solid','CompositorNodeRGB', 'SNAP_FACE']
source_node_data['GROUP'] = ['Compositor','CompositorNodeGroup', 'NODE_COMPOSITING']

output_node_data = {}
output_node_data['COMPOSITE'] = ['Composite', 'CompositorNodeComposite', 'NODE_COMPOSITING']
output_node_data['OUTPUT_FILE'] = ['File Output', 'CompositorNodeOutputFile', 'OUTPUT']

layer_node_data = {}
layer_node_data['IMAGE'] = ['Image', 'CompositorNodeImage', 'OUTLINER_OB_IMAGE']
layer_node_data['MOVIECLIP'] = ['Movie Clip', 'CompositorNodeMovieClip', 'SEQUENCE']
layer_node_data['RGB'] = ['Solid','CompositorNodeRGB', 'SNAP_FACE']
layer_node_data['TEX_GRADIENT'] = ['Gradient Texture', 'ShaderNodeTexGradient', 'NODE_TEXTURE']

texture_node_data = {}
texture_node_data['TEXTURE'] = ['Texture', 'CompositorNodeTexture', 'TEXTURE']
texture_node_data['TEX_BRICK'] = ['Brick Texture', 'ShaderNodeTexBrick', 'TEXTURE']
texture_node_data['TEX_CHECKER'] = ['Checker Texture', 'ShaderNodeTexChecker', 'TEXTURE']
texture_node_data['TEX_GABOR'] = ['Gabor Texture', 'ShaderNodeTexGabor', 'TEXTURE']
texture_node_data['TEX_GRADIENT'] = ['Gradient Texture', 'ShaderNodeTexGradient', 'TEXTURE']
texture_node_data['TEX_MAGIC'] = ['Magic Texture', 'ShaderNodeTexMagic', 'TEXTURE']
texture_node_data['TEX_NOISE'] = ['Noise Texture', 'ShaderNodeTexNoise', 'TEXTURE']
texture_node_data['TEX_VORONOI'] = ['Voronoi Texture', 'ShaderNodeTexVoronoi', 'TEXTURE']
texture_node_data['TEX_WAVE'] = ['Wave Texture', 'ShaderNodeTexWave', 'TEXTURE']
texture_node_data['TEX_WHITE_NOISE'] = ['White Noise Texture', 'ShaderNodeTexWhiteNoise', 'TEXTURE']

feature_node_data = {}
feature_node_data['CompositorNodeFill'] = ['Fill', 'CompositorNodeFill', 'SNAP_FACE']
feature_node_data['CompositorNodeSpotFill'] = ['Spot Fill', 'CompositorNodeSpotFill', 'SURFACE_NCIRCLE']
feature_node_data['CompositorNodeColorSelection'] = ['ColorSelection', 'CompositorNodeColorSelection', 'VIS_SEL_11']
feature_node_data['CompositorNodeReplaceColor'] = ['Replace Color', 'CompositorNodeReplaceColor', 'OVERLAY']
feature_node_data['CompositorNodeInnerShadow'] = ['InnerShadow', 'CompositorNodeInnerShadow', 'ANTIALIASED']
feature_node_data['CompositorNodeInnerShadowSingle'] = ['InnerShadow(Single)', 'CompositorNodeInnerShadowSingle', 'ANTIALIASED']
feature_node_data['CompositorNodeBoundaryLine'] = ['BoundaryLine', 'CompositorNodeBoundaryLine', 'MOD_LINEART']
feature_node_data['CompositorNodeSpotExposure'] = ['Spot Exposure', 'CompositorNodeSpotExposure', 'LIGHT_SPOT']
feature_node_data['CompositorNodeCameraLensBlur'] = ['Camera Lens Blur', 'CompositorNodeCameraLensBlur', 'VIEW_CAMERA']
feature_node_data['CompositorNodeChromaticAberration'] = ['Chromatic Aberration', 'CompositorNodeChromaticAberration', 'SEQ_CHROMA_SCOPE']
feature_node_data['CompositorNodeVignette'] = ['Vignette', 'CompositorNodeVignette', 'MOD_MASK']
feature_node_data['CompositorNodeEdgeSoftness'] = ['Edge Softness', 'CompositorNodeEdgeSoftness', 'PROP_OFF']
feature_node_data['CompositorNodeSwingTilt'] = ['Swing-Tilt', 'CompositorNodeSwingTilt', 'AREA_SWAP']
feature_node_data['CompositorNodeShutterStreak'] = ['Shutter Streak', 'CompositorNodeShutterStreak', 'CAMERA_STEREO']
feature_node_data['CompositorNodeBlurRGB'] = ['Blur RGB', 'CompositorNodeBlurRGB', 'PROP_CON']
feature_node_data['CompositorNodeTwitch'] = ['Twitch', 'CompositorNodeTwitch', 'GHOST_ENABLED']
feature_node_data['CompositorNodeRenoiser'] = ['Renoiser', 'CompositorNodeRenoiser', 'TEXTURE']
feature_node_data['CompositorNodeWiggleTransfrom'] = ['Wiggle Transfrom', 'CompositorNodeWiggleTransfrom', 'CON_ROTLIKE']
feature_node_data['CompositorNodeSeparateRGBA'] = ['Separate RGBA', 'CompositorNodeSeparateRGBA', 'PARTICLES']

feature_node_data_4_5 = ['CompositorNodeSwingTilt', 'CompositorNodeTwitch', 'CompositorNodeWiggleTransfrom']

socket_data = {}
socket_data['RGBA'] = 'NODE_SOCKET_RGBA'
socket_data['VALUE'] = 'NODE_SOCKET_FLOAT'
socket_data['VECTOR'] = 'NODE_SOCKET_VECTOR'