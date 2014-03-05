import sublime, sublime_plugin
import os
from subprocess import Popen

WINMERGE = ""
if sublime.platform() == "windows":
	import _winreg

	WINMERGE = _winreg.QueryValue(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\WinMergeU.exe')

	if not WINMERGE:
		if os.path.exists("%s\WinMerge\WinMergeU.exe" % os.environ['ProgramFiles(x86)']):
			WINMERGE = '"%s\WinMerge\WinMergeU.exe"' % os.environ['ProgramFiles(x86)']
		else:
			WINMERGE = '"%s\WinMerge\WinMergeU.exe"' % os.environ['ProgramFiles']
elif sublime.platform() == "osx":
	WINMERGE = "/usr/bin/opendiff"

fileA = fileB = None

def recordActiveFile(f):
	global fileA
	global fileB
	fileB = fileA
	fileA = f

class WinMergeCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		cmd_line = ''
		bShell = False
		if sublime.platform() == "windows":
			cmd_line = '%s /e /ul /ur "%s" "%s"' % (WINMERGE, fileB, fileA)
		elif sublime.platform() == "osx":
			cmd_line = '%s "%s" "%s"' % (WINMERGE, fileB, fileA)
			bShell = True
		print "WinMerge command: " + cmd_line
		Popen(cmd_line, shell=bShell)

class WinMergeFileListener(sublime_plugin.EventListener):
	def on_activated(self, view):
		if view.file_name() != fileA:
			recordActiveFile(view.file_name())

