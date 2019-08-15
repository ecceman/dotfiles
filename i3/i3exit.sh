#!/bin/sh

case "$1" in
	logout)
		i3-msg exit
		;;
	reboot)
		systemctl reboot
		;;
	poweroff)
		systemctl poweroff
		;;
	*)
		exit 2
esac
