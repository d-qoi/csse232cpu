package edu.rose_hulman.csse232.groupM;

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;

import javax.swing.JFrame;
import javax.swing.JTextArea;
import javax.swing.text.Highlighter;
import javax.swing.text.BadLocationException;
import javax.swing.text.DefaultHighlighter;

public class DebugInstructionFrame extends JFrame {
	private static final long serialVersionUID = -7110874263911295767L;
	
	public JTextArea text;
	
	public DebugInstructionFrame() {
		super();
		text = new JTextArea();
		text.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 12));
		text.setEditable(false);
		this.add(text);
		this.setSize(200, 550);
		this.setResizable(false);
		text.setSize(text.getSize());
		this.setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
	}
	
	@Override
	public void update(Graphics g) {
		super.update(g);
	}
	
	public void update(Emulator emu) {
		int pc = emu.getRegister((short) 3);
		int ra = emu.getRegister((short) 5);
		int lower = pc - 15;
		int upper = pc + 15;
		//convert to line #s
		ra = (ra - pc);
		pc = (pc - lower);
		ra += pc;
		String instructions = emu.debugInstructions(lower, upper);
		text.setText(instructions);
		Highlighter h = text.getHighlighter();
		h.removeAllHighlights();
		int[] indexes = getIndexesOfLine(pc);
		try {
			h.addHighlight(indexes[0], indexes[1], new DefaultHighlighter.DefaultHighlightPainter(Color.YELLOW));
			if ((ra >= 0) && (ra < 30)) { //if ra is on a rendered line
				indexes = getIndexesOfLine(ra);
				h.addHighlight(indexes[0], indexes[1], new DefaultHighlighter.DefaultHighlightPainter(Color.CYAN));
			}
		} catch (BadLocationException e) {
			e.printStackTrace();
		}
		text.setCaretPosition(text.getDocument().getLength());
		this.repaint();
	}
	
	private int[] getIndexesOfLine(int ln) {
		String[] lines = text.getText().split("\n");
		int[] index = new int[]{0,0};
		if (lines.length == 1)
			return index;
//		System.out.printf("Getting line %d [%d]%n", ln, lines.length);
		for (int i = 0; i < ln; i++) {
			index[0] += (lines[i].length()) + 1;
		}
		index[1] = index[0] + lines[ln].length();
		return index;
	}

}
