# VMI ECE Robot Object Detection
## _2022 IEEE SoutheastCon Hardware Competition_

Built using the jetson-inference repository, this project provides visual objection detection for a robot capable of autonomous line-tracking znd retrieiving/throwing beads. The hardware used for the object detection is a NVIDIA Jetson Nano 4GB and generic CSI camera.

Trained on 1500+ self-taken images. the customly built training model was on:
- Mardi-Gras style beads of various color
- Red Solo cups
- Small nets attached to a wooden dowel

The main python code is for handling different states of the robot based on the objects detected (i.e. if robot catapault is empty and beads are detected then align, stop driving and retrieve beads). Communication is passed using GPIO to the main Arduino bus.

VMI's team consisted of 14 members with 2 members focused on computer vision. The robot design qualified for the finals in a 28 team competition. Small clips/videos of the testing phase posted later.
