# blender <your_scene>.blend --background --python export_fbx.py -- <your_scene>.fbx
# https://stackoverflow.com/a/64857797

import bpy
import os, shutil
# import zipfile
# from datetime import datetime

def setup_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)

# def make_zipfile(output_filename, source_dir):
#     with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zip:
#         for root, dirs, files in os.walk(source_dir):
#             # add directory (needed for empty dirs)
#             if not os.path.relpath(root, source_dir).startswith('.'):
#                 zip.write(root, os.path.relpath(root, source_dir))

#             for file in files:
#                 if file.endswith('.blend1') or file.startswith('.') or file == output_filename:
#                     continue

#                 filename = os.path.join(root, file)
#                 if os.path.isfile(filename): # regular files only
#                     arcname = os.path.join(os.path.relpath(root, source_dir), file)
#                     zip.write(filename, arcname)

# filepath = sys.argv[-1]

# export to blend file location
basedir = os.path.dirname(bpy.data.filepath)
if not basedir:
    raise Exception("Blend file not found.")

fbxdir = os.path.join(basedir, 'fbx')
objdir = os.path.join(basedir, 'obj')
gltfdir = os.path.join(basedir, 'gltf')

# Create the format directories if they don't already exist
setup_dir(fbxdir)
setup_dir(objdir)
setup_dir(gltfdir)

view_layer = bpy.context.view_layer

bpy.ops.object.select_all(action='DESELECT')

for obj in bpy.data.collections['Assets'].all_objects:
    obj.select_set(True)

    # some exporters only use the active object
    view_layer.objects.active = obj

    # Export FBX
    name = bpy.path.clean_name(obj.name) + ".fbx"
    filepath = os.path.join(fbxdir, name)
    bpy.ops.export_scene.fbx(filepath=filepath, use_selection=True)

    # Export OBJ
    name = bpy.path.clean_name(obj.name) + ".obj"
    filepath = os.path.join(objdir, name)
    bpy.ops.export_scene.obj(filepath=filepath, use_selection=True)

    # Export GLTF
    name = bpy.path.clean_name(obj.name) + ".gltf"
    filepath = os.path.join(gltfdir, name)
    bpy.ops.export_scene.gltf(filepath=filepath, use_selection=True)

    obj.select_set(False)

# filename = os.path.splitext(bpy.data.filepath)[0]
# timestamp = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
# make_zipfile(filename + "-" + timestamp + ".zip", basedir)