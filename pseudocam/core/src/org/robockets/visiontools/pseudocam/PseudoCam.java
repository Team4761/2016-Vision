package org.robockets.visiontools.pseudocam;

import com.badlogic.gdx.ApplicationAdapter;
import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.GL20;
import com.badlogic.gdx.graphics.g2d.BitmapFont;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.graphics.glutils.ShapeRenderer;
import edu.wpi.first.wpilibj.networktables.NetworkTable;

public class PseudoCam extends ApplicationAdapter {
	private ShapeRenderer shapeRenderer;
	private SpriteBatch batch;
	private BitmapFont font;
	private float width;
	private float height;

	private NetworkTable visionTable;
	private double bbBottomLeftX;
	private double bbBottomLeftY;
	private double bbWidth;
	private double bbHeight;
	private double canSeeTarget;
	private double distance;
	
	@Override
	public void create() {
		width = Gdx.graphics.getWidth();
		height = Gdx.graphics.getHeight();
		shapeRenderer = new ShapeRenderer();
		batch = new SpriteBatch();
		font = new BitmapFont();
		font.setColor(Color.WHITE);

		NetworkTable.setClientMode();
		NetworkTable.setIPAddress("roborio-4761-frc.local");
		visionTable = NetworkTable.getTable("vision");
	}

	@Override
	public void render() {
		refreshNetworkTableValues();
		Gdx.gl.glClearColor(0, 0, 0, 1);
		Gdx.gl.glClear(GL20.GL_COLOR_BUFFER_BIT);
		shapeRenderer.begin(ShapeRenderer.ShapeType.Filled);
		if(!visionTable.isConnected()) {
			shapeRenderer.setColor(Color.YELLOW);
		}
		else if(canSeeTarget == 1.0) {
			shapeRenderer.setColor(Color.GREEN);
		}
		else {
			shapeRenderer.setColor(Color.RED);
		}
		shapeRenderer.rect((float) bbBottomLeftX, (float) bbBottomLeftY, (float) bbWidth, (float) bbHeight);
		shapeRenderer.setColor(Color.WHITE);
		shapeRenderer.rectLine(width / 2, 0, width / 2, height, 3);
		shapeRenderer.end();

		batch.begin();
		font.draw(batch, String.format("Distance: %g feet", distance), 5, font.getLineHeight());
		batch.end();
	}

	private void refreshNetworkTableValues() {
		bbWidth = visionTable.getNumber("width", 50);
		bbHeight = visionTable.getNumber("height", 50);
		bbBottomLeftX = visionTable.getNumber("topleft_x", 0);
		bbBottomLeftY = height - visionTable.getNumber("topleft_y", 50);
		canSeeTarget = visionTable.getNumber("can_see_target", 0);
		distance = visionTable.getNumber("distance_guess", 0);
	}
}
