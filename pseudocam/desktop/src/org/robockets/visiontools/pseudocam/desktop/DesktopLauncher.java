package org.robockets.visiontools.pseudocam.desktop;

import com.badlogic.gdx.backends.lwjgl.LwjglApplication;
import com.badlogic.gdx.backends.lwjgl.LwjglApplicationConfiguration;
import org.robockets.visiontools.pseudocam.PseudoCam;

public class DesktopLauncher {
	public static void main (String[] arg) {
		LwjglApplicationConfiguration config = new LwjglApplicationConfiguration();
		config.resizable = false;
		config.width = 640;
		config.height = 480;
		new LwjglApplication(new PseudoCam(), config);
	}
}
