#!/usr/bin/env python
# encoding: UTF-8
# migrate volumes in new pools
# author: Sébastien Boisvert

import os

def runCommand(commmand):
	print(commmand)
	return
	#os.system(commmand)

volumes = []

for line in open("volumes.txt"):
	volumes.append(line.strip())

for volume in volumes:

	if volume == "":
		continue

	runCommand("# Migrating volume " + volume)

	runCommand("virsh vol-download " + volume + " blob virtualization")
	newVolumeName = volume + "-migrated"
	runCommand("stat -c %s blob > volume-capacity")

	newPool = "domain-images"

	if volume.find("domains.") == 0:

		newVolumeName = volume.replace("domains.", "")
		newPool = "domain-images"

	elif volume.find("ISO-images.") == 0:

		newVolumeName = volume.replace("ISO-images.", "")
		newPool = "iso-images"

	elif volume.find("pristine-images.") == 0:

		newVolumeName = volume.replace("pristine-images.", "")
		newPool = "pristine-images"

	
	runCommand("virsh vol-create-as " + newPool + " " + newVolumeName + " $(cat volume-capacity)")

	runCommand("virsh vol-upload " + newVolumeName + " blob " + newPool)

	runCommand("virsh vol-delete " + volume + " virtualization")

	runCommand("")
