# Copyright (c) 2018 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
Hook which chooses an environment file to use based on the current context.
"""

from tank import Hook
import sgtk, sys

class PickEnvironment(Hook):
    def execute(self, context, **kwargs):
        """
        The default implementation assumes there are three environments, called shot, asset
        and project, and switches to these based on entity type.
        """

        # Get the engine instance that is currently running.

        if context.source_entity:
            if context.source_entity["type"] == "Version":
                return "version"
            elif context.source_entity["type"] == "PublishedFile":
                return "publishedfile"
            elif context.source_entity["type"] == "Playlist":
                return "playlist"
            elif context.source_entity["type"] == "CustomEntity03":
                return "material"
            elif context.source_entity["type"] == "CustomEntity02":
                return "scene"
            elif context.source_entity["type"] == "CustomEntity01":
                return "material_family" 

        if context.project is None:
            # Our context is completely empty. We're going into the site context.
            return "site"

        if context.entity is None:
            # We have a project but not an entity.
            return "project"

        if context.entity and context.step is None:
            # We have an entity but no step.
            if context.entity["type"] == "Shot": 
                sg_shot=self.parent.shotgun.find_one("Shot", [["id", "is", context.entity["id"]]], ["sg_shot_type"])
                shot_type=sg_shot["sg_shot_type"]
                if shot_type == "Showroom":
                    return "showroom"
                else:
                    return "shot"
            if context.entity["type"] == "Asset":
                return "asset"
            if context.entity["type"] == "Sequence":
                return "sequence"
            if context.entity["type"] == "Episode":
                return "episode" 
            if context.entity["type"] == "CustomEntity03": 
                return "material"
            if context.entity["type"] == "CustomEntity02": 
                return "scene"
            if context.entity["type"] == "Asset":
                return "asset"
            if context.entity["type"] == "Sequence":
                return "sequence"
            if context.entity["type"] == "Episode":
                return "episode" 
            if context.entity["type"] == "CustomEntity03": 
                return "material"
            if context.entity["type"] == "CustomEntity02": 
                return "scene"
            if context.entity["type"] == "CustomEntity01": 
                return "material_family"

        if context.entity and context.step:
            # We have a step and an entity.     
            if context.entity["type"] == "Shot":
                sg_shot=self.parent.shotgun.find_one("Shot", [["id", "is", context.entity["id"]]], ["sg_shot_type"])
                shot_type=sg_shot["sg_shot_type"]
                if shot_type == "Showroom":
                    if context.step["name"] == "AR":
                        return "showroom_step_ar"
                    elif context.step["name"] == "SPR":
                        return "showroom_step_sprite"
                    elif context.step["name"] == "DFT":
                        return "showroom_step_render"
                    elif context.step["name"] == "RND":
                        return "showroom_step_render"
                    else: 
                        # shot_type is showroom and step is none of the above
                        return "showroom_step_post"
                else: 
                    # shot_type is not showroom
                    if context.step["name"] == "DFT":
                            return "shot_step_render"
                    elif context.step["name"] == "RND":
                            return "shot_step_render"
                    elif context.step["name"] == "PST":
                        return "shot_step_post"
                    else:
                        # shot_type is not showroom and step is none of the above
                        return "shot_step"
            if context.entity["type"] == "Asset":
                return "asset_step"
            if context.entity["type"] == "CustomEntity03":
                return "material_step"
            if context.entity["type"] == "CustomEntity02":
                return "scene_step"
        return None
