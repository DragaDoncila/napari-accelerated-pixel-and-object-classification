from apoc import PredefinedFeatureSet, PixelClassifier, ObjectSegmenter, ObjectClassifier, ProbabilityMapper

import numpy as np
from napari_plugin_engine import napari_hook_implementation

import napari
from napari_time_slicer import time_slicer
from napari_tools_menu import register_function

@napari_hook_implementation
def napari_experimental_provide_function():
    return [
        Train_object_segmentation,
        Apply_object_segmentation,
        Apply_probability_mapper,
        Train_object_segmentation_from_visible_image_layers,
        Apply_object_segmentation_to_visible_image_layers,
        Train_pixel_classifier,
        Apply_pixel_classification,
        Train_pixel_classifier_from_visible_image_layers,
        Apply_pixel_classification_to_visible_image_layers,
        Connected_component_labeling, Train_object_classifier, Apply_object_classification]

def Train_pixel_classifier(
        image: "napari.types.ImageData",
        annotation : "napari.types.LabelsData",
        model_filename : str = "PixelClassifier.cl",
        featureset : PredefinedFeatureSet = PredefinedFeatureSet.small_quick,
        custom_features : str = "original gaussian_blur=1 sobel_of_gaussian_blur=1",
        max_depth : int = 2,
        num_ensembles : int = 10
) -> "napari.types.LabelsData":
    feature_stack = featureset.value
    if feature_stack == "":
        feature_stack = custom_features

    clf = PixelClassifier(opencl_filename=model_filename, num_ensembles=num_ensembles, max_depth=max_depth)
    clf.train(feature_stack, annotation, image)

    result = clf.predict(features=feature_stack, image=image)
    return result

@register_function(menu="Segmentation / labeling > Semantic segmentation (apply pretrained, APOC)")
@time_slicer
def Apply_pixel_classification(image: "napari.types.ImageData",
                               model_filename : str = "PixelClassifier.cl",
                               viewer: napari.Viewer = None) -> "napari.types.LabelsData":

    clf = PixelClassifier(opencl_filename=model_filename)
    result = clf.predict(image=image)
    return result

def Train_pixel_classifier_from_visible_image_layers(
        annotation : "napari.types.LabelsData",
        model_filename : str = "PixelClassifier.cl",
        featureset : PredefinedFeatureSet = PredefinedFeatureSet.small_quick,
        custom_features : str = "original gaussian_blur=1 sobel_of_gaussian_blur=1",
        max_depth : int = 2,
        num_ensembles : int = 10,
        napari_viewer : napari.Viewer = None
) -> "napari.types.LabelsData":
    image = [layer.data for layer in napari_viewer.layers if (isinstance(layer, napari.layers.Image) and layer.visible)]

    feature_stack = featureset.value
    if feature_stack == "":
        feature_stack = custom_features

    clf = PixelClassifier(opencl_filename=model_filename, num_ensembles=num_ensembles, max_depth=max_depth)
    clf.train(feature_stack, annotation, image)

    result = clf.predict(features=feature_stack, image=image)
    return result

def Apply_pixel_classification_to_visible_image_layers(
        model_filename : str = "PixelClassifier.cl",
        napari_viewer : napari.Viewer = None
) -> "napari.types.LabelsData":
    image = [layer.data for layer in napari_viewer.layers if (isinstance(layer, napari.layers.Image) and layer.visible)]

    clf = PixelClassifier(opencl_filename=model_filename)
    result = clf.predict(image=image)
    return result

def Train_object_segmentation(
        image: "napari.types.ImageData",
        annotation : "napari.types.LabelsData",
        model_filename : str = "ObjectSegmenter.cl",
        featureset : PredefinedFeatureSet = PredefinedFeatureSet.small_quick,
        custom_features : str = "original gaussian_blur=1 sobel_of_gaussian_blur=1",
        max_depth : int = 2,
        num_ensembles : int = 10,
        annotated_object_intensity : int = 2
) -> "napari.types.LabelsData":
    feature_stack = featureset.value
    if feature_stack == "":
        feature_stack = custom_features

    clf = ObjectSegmenter(opencl_filename=model_filename, num_ensembles=num_ensembles, max_depth=max_depth, positive_class_identifier=annotated_object_intensity)
    clf.train(feature_stack, annotation, image)

    result = clf.predict(feature_stack, image)
    return result


@register_function(menu="Filtering > Probability Mapper (apply pretrained, APOC)")
@time_slicer
def Apply_probability_mapper(image: "napari.types.ImageData",
                              model_filename : str = "ProbabilityMapper.cl",
                              viewer: napari.Viewer = None) -> "napari.types.ImageData":
    clf = ProbabilityMapper(opencl_filename=model_filename)
    result = clf.predict(image=image)
    return result


@register_function(menu="Segmentation / labeling > Object segmentation (apply pretrained, APOC)")
@time_slicer
def Apply_object_segmentation(image: "napari.types.ImageData",
                              model_filename : str = "ObjectSegmenter.cl",
                              viewer: napari.Viewer = None) -> "napari.types.LabelsData":
    clf = ObjectSegmenter(opencl_filename=model_filename)
    result = clf.predict(image=image)
    return result

def Train_object_segmentation_from_visible_image_layers(
        annotation : "napari.types.LabelsData",
        model_filename : str = "object_segmenter.cl",
        featureset : PredefinedFeatureSet = PredefinedFeatureSet.small_quick,
        custom_features : str = "original gaussian_blur=1 sobel_of_gaussian_blur=1",
        max_depth : int = 2,
        num_ensembles : int = 10,
        annotated_object_intensity : int = 2,
        napari_viewer : napari.Viewer = None
) -> "napari.types.LabelsData":
    image = [layer.data for layer in napari_viewer.layers if (isinstance(layer, napari.layers.Image) and layer.visible)]

    feature_stack = featureset.value
    if feature_stack == "":
        feature_stack = custom_features

    clf = ObjectSegmenter(opencl_filename=model_filename, num_ensembles=num_ensembles, max_depth=max_depth, positive_class_identifier=annotated_object_intensity)
    clf.train(feature_stack, annotation, image)

    result = clf.predict(features=feature_stack, image=image)
    return result

def Apply_object_segmentation_to_visible_image_layers(
        model_filename : str = "ObjectSegmenter.cl",
        napari_viewer : napari.Viewer = None
) -> "napari.types.LabelsData":
    image = [layer.data for layer in napari_viewer.layers if (isinstance(layer, napari.layers.Image) and layer.visible)]

    clf = ObjectSegmenter(opencl_filename=model_filename)
    result = clf.predict(image=image)
    return result


def Connected_component_labeling(labels: "napari.types.LabelsData", object_class_identifier : int = 2, fill_gaps_between_labels:bool = True) -> "napari.types.LabelsData":
    import pyclesperanto_prototype as cle
    binary = cle.equal_constant(labels, constant=object_class_identifier)
    if fill_gaps_between_labels:
        instances = cle.voronoi_labeling(binary)
    else:
        instances = cle.connected_components_labeling_box(binary)
    return instances


def Train_object_classifier(image: "napari.types.ImageData",
        labels : "napari.types.LabelsData",
        annotation : "napari.types.LabelsData",
        model_filename : str = "ObjectClassifier.cl",
        max_depth : int = 2,
        num_ensembles : int = 10,
        area : bool = True,
        min_intensity: bool = False,
        mean_intensity: bool = False,
        max_intensity: bool = False,
        sum_intensity: bool = False,
        standard_deviation_intensity: bool = False,
        shape: bool = False,
        position:bool = False,
        touching_neighbor_count:bool = False,
        average_distance_of_touching_neighbors:bool = False,
        distance_to_nearest_neighbor:bool = False,
        average_distance_to_6_nearest_neighbors:bool = False,
        average_distance_to_10_nearest_neighbors:bool = False,
    ) -> "napari.types.LabelsData":

    features = ","
    if area:
        features = features + "area,"
    if min_intensity:
        features = features + "min_intensity,"
    if mean_intensity:
        features = features + "mean_intensity,"
    if max_intensity:
        features = features + "max_intensity,"
    if sum_intensity:
        features = features + "sum_intensity,"
    if standard_deviation_intensity:
        features = features + "standard_deviation_intensity,"
    if shape:
        features = features + "mean_max_distance_to_centroid_ratio,"
    if position:
        features = features + "centroid_x,centroid_y,centroid_z,"
    if touching_neighbor_count:
        features = features + "touching_neighbor_count,"
    if average_distance_of_touching_neighbors:
        features = features + "average_distance_of_touching_neighbors,"
    if distance_to_nearest_neighbor:
        features = features + "average_distance_of_n_nearest_neighbors=1,"
    if average_distance_to_6_nearest_neighbors:
        features = features + "average_distance_of_n_nearest_neighbors=6,"
    if average_distance_to_10_nearest_neighbors:
        features = features + "average_distance_of_n_nearest_neighbors=10,"

    features = features[1:-1]

    clf = ObjectClassifier(opencl_filename=model_filename, num_ensembles=num_ensembles,
                                           max_depth=max_depth)

    clf.train(features, labels, annotation, image)
    result = clf.predict(labels, image)
    return result

@register_function(menu="Segmentation post-processing > Object classification (apply pretrained, APOC)")
@time_slicer
def Apply_object_classification(image: "napari.types.ImageData",
                             labels: "napari.types.LabelsData",
                             model_filename : str = "ObjectClassifier.cl",
                             viewer: napari.Viewer = None) -> "napari.types.LabelsData":

    clf = ObjectClassifier(opencl_filename=model_filename)
    result = clf.predict(labels, image)
    return result
