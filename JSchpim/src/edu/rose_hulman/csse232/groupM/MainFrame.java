package edu.rose_hulman.csse232.groupM;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Image;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;

import javax.imageio.ImageIO;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;
import javax.sound.sampled.FloatControl;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JSeparator;
import javax.swing.JSplitPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.SwingWorker;

public class MainFrame extends JFrame implements ActionListener {
	private static final long serialVersionUID = -5979979493835436236L;
	
	public static final short DEFAULT_SP = (short) 0xfff0;
	public static final short DEFAULT_PC = (short) 0x1000;
	
	private Emulator emu;
	
	private JScrollPane scroll;
	private JTextArea console;
	private JTextArea instructionMem;
	private JTextArea dataMem;
	private StaticRegisterPanel staticRegs;
	private SchwapPanel schwapRegs;
	private RunEmulatorTask task;
	private DebugInstructionFrame debug;
	
	public void actionPerformed(ActionEvent e) {
		switch (e.getActionCommand()) {
			case "Reset":
				emu.write("Reset emulator!");
				for (short i = 0; i < 16; i++) {
					emu.setRegister(i, (short) 0);
				}
				emu.setRegister((short) 3, DEFAULT_PC);
				emu.setRegister((short) 4, DEFAULT_SP);
				emu.mem.clear();
				emu.halt = false;
				update();
				break;
			case "Load":
				JFileChooser chooser = new JFileChooser();
			    int returnVal = chooser.showOpenDialog(this);
			    if(returnVal == JFileChooser.APPROVE_OPTION) {
			    	emu.write("Loading assembly file: " +
			            chooser.getSelectedFile().getName());
			       	try {
						Scanner sc = new Scanner(chooser.getSelectedFile());
						ArrayList<String> al = new ArrayList<String>();
						ArrayList<Integer> breakPoints = new ArrayList<Integer>();
						al.add("#" + Integer.toHexString(MainFrame.DEFAULT_PC));
						String str;
						int line = 0;
						while (sc.hasNextLine()) {
							if ((str=sc.nextLine().trim()).startsWith("*")) {
								str = str.substring(1);
								if (str.startsWith("0x"))
									breakPoints.add(line);
							}
							if ((str).startsWith("0x")) {
								al.add(str);
								line++;
							} else if (str.startsWith("#"))
								al.set(0, str);
						}
						String[] arr = new String[0];
						arr = al.toArray(arr);
						sc.close();
						emu.loadDataMemory(arr);
						int pc = emu.getRegister((short) 3);
						for (Integer i : breakPoints) {
							emu.setBreakpoint(pc + (2*i.intValue()));
						}
						update();
					} catch (FileNotFoundException e1) {
						e1.printStackTrace();
						emu.write(e1.getMessage());
					}
			    }
			    break;
			case "Clear":
				console.setText("");
				emu.write("Console cleared!");
				update();
				break;
			case "Step":
				emu.step();
				update();
				break;
			case "<":
				schwapRegs.schwap = ((schwapRegs.schwap - 1) + SchwapPanel.schwapMod) % SchwapPanel.schwapMod;
				schwapRegs.update(schwapRegs.schwap);
				break;
			case ">":
				schwapRegs.schwap = ((schwapRegs.schwap + 1)) % SchwapPanel.schwapMod;
				schwapRegs.update(schwapRegs.schwap);
				break;
			case "Run":
				if (this.task == null)
					this.task = new RunEmulatorTask();
				this.task.execute();
				break;
			case "Pause":
				this.task.cancel(false);
				this.task = null;
			default: return;
		}
	}
	
	public MainFrame() {
		super("JSchpim");
		emu = new Emulator(DEFAULT_SP, DEFAULT_PC);
		emu.setConsoleStream(new ConsoleStream());
		try {
			this.setIconImage(ImageIO.read(new File("cpu.gif")));
		}
		catch (IOException exc) {
		    exc.printStackTrace();
		}
		// Easter eggs & memes
		this.addWindowListener(new IlluminatiWindowListener());
		// Actual code
		this.task = new RunEmulatorTask();
		this.setLayout(new BorderLayout());
		JPanel buttonsPanel = new JPanel();
		buttonsPanel.add(makeButton("Reset"));
		buttonsPanel.add(makeButton("Load"));
		buttonsPanel.add(makeButton("Clear"));
		buttonsPanel.add(makeButton("Step"));
		buttonsPanel.add(makeButton("Run"));
		buttonsPanel.add(makeButton("Pause"));
		this.add(buttonsPanel, BorderLayout.NORTH);
		JSplitPane main = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT);
		JPanel registerPanel = new JPanel(new BorderLayout());
		registerPanel.add(staticRegs = new StaticRegisterPanel(), BorderLayout.NORTH);
		registerPanel.add(schwapRegs = new SchwapPanel(), BorderLayout.CENTER);
		main.add(registerPanel);
		JSplitPane leftPanel = new JSplitPane(JSplitPane.VERTICAL_SPLIT);
		leftPanel.add(scroll = new JScrollPane(console = new JTextArea()));
		console.setEditable(false);
		console.setForeground(Color.RED);
		console.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 12));
		scroll.setPreferredSize(new Dimension(600, 200));
		JSplitPane mem = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT);
		mem.add(instructionMem = new JTextArea());
		mem.add(dataMem = new JTextArea());	
		instructionMem.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 12));
		dataMem.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 12));
		leftPanel.add(mem);
		main.add(leftPanel);
		instructionMem.setEditable(false);
		instructionMem.setPreferredSize(new Dimension(200, 100));
		dataMem.setEditable(false);
		this.add(main, BorderLayout.CENTER);
		debug = new DebugInstructionFrame();
		update();
		debug.setVisible(true);
		this.pack();
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		this.setVisible(true);
		emu.write("Initialized emulator @ $SP=%04x, $PC=%04x", emu.getRegister((short) 4), emu.getRegister((short) 3));
		emu.write("NOTE:\tThe machine code file should have 1 instruction per line in form 0x[Hex value]");
		emu.write("\tInvalid and empty lines will be ignored. Lines that start with * will have a breakpoint placed there.");
		emu.write("\tStarting the file with #[Hex value], will load the program into the specified hex address");
		emu.write("Syscall 10 => print\nSyscall 0 ==> exit");
	}
	
	public JButton makeButton(String caption) {
		JButton b = new JButton(caption);
        b.setActionCommand(caption);
        b.addActionListener(this);
        b.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 14));
        b.setFocusable(false);
        return b;
	}
	
	/**
	 * Updates the objects (Registers, console, etc.)
	 */
	public void update() {
		// Update registers
		staticRegs.update();
		schwapRegs.update(emu.getActiveSchwap());
		// Update Memory - Figure out exact sizes later
		instructionMem.setText(emu.debugInstructions(10));
		dataMem.setText(emu.debugMemory(10));
		debug.update(emu);
	}
	
	public void update(Graphics g) {
		this.update();
		super.update(g);
	}
	
	public static void main(String[] args) {
		new MainFrame();
	}
	
	private class StaticRegisterPanel extends JPanel {
		private static final long serialVersionUID = 1351961192950438805L;
		private JTextField registers[];
		
		public StaticRegisterPanel() {
			super();
			GridBagLayout grid = new GridBagLayout();
			this.setLayout(grid);
			RegisterName[] names = RegisterName.values();
			GridBagConstraints c = new GridBagConstraints();
			registers = new JTextField[names.length];
			JLabel label;
			for (c.gridy = 0; c.gridy < names.length; c.gridy++) {
				label = new JLabel(names[c.gridy].name());
				label.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 12));
				c.gridx = 0;
				c.weightx = 0.5;
				c.anchor = GridBagConstraints.LINE_START;
				c.fill = GridBagConstraints.NONE;
				this.add(label, c);
				c.gridx = 1;
				c.weightx = 1;
				c.anchor = GridBagConstraints.LINE_END;
				c.fill = GridBagConstraints.HORIZONTAL;
				this.add(registers[c.gridy] = new JTextField(Integer.toHexString(emu.getRegister((short) c.gridy))), c); 
				registers[c.gridy].setFont(new Font(Font.MONOSPACED, Font.PLAIN, 14));
				registers[c.gridy].setMinimumSize(new Dimension(100, 20));
			}
			for (int i = 0; i < registers.length; i++) {
				registers[i].setEditable(false);
				registers[i].setBackground(Color.WHITE);
			}
		}

		public void update() {
			for (int i = 0; i < registers.length; i++) {
				registers[i].setText(Integer.toHexString(emu.getRegister((short) i)));
			}
		}
	}
	
	private class SchwapPanel extends JPanel {
		private static final long serialVersionUID = 6176462482893112268L;

		public int schwap;
		private static final int schwapMod = 16;
		
		private JLabel schwapLabel;
		
		private JTextField[] registers;
		
		public SchwapPanel() {
			super(new BorderLayout());
			schwap = 0;
			registers = new JTextField[4];
			JPanel top = new JPanel(new BorderLayout());
			top.add(new JSeparator(), BorderLayout.NORTH);
			top.add(makeButton(">"), BorderLayout.EAST);
			top.add(makeButton("<"), BorderLayout.WEST);
			top.add(schwapLabel = new JLabel(getSwapString()), BorderLayout.CENTER);
			schwapLabel.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 12));
			this.add(top, BorderLayout.NORTH);
			JPanel regs = new JPanel(new GridBagLayout());
			GridBagConstraints c = new GridBagConstraints();
			JLabel label;
			for (c.gridy = 0; c.gridy < 4; c.gridy++) {
				c.gridx = 0;
				c.weightx = 0.5;
				c.anchor = GridBagConstraints.LINE_START;
				c.fill = GridBagConstraints.NONE;
				label = new JLabel("$h" + c.gridy);
				label.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 12));
				regs.add(label, c);
				c.gridx = 1;
				c.weightx = 1;
				c.anchor = GridBagConstraints.LINE_END;
				c.fill = GridBagConstraints.HORIZONTAL;
				regs.add(registers[c.gridy] = new JTextField(Integer.toHexString(emu.getSchwapRegister((short) schwap,(short) c.gridy))), c);
				registers[c.gridy].setFont(new Font(Font.MONOSPACED, Font.PLAIN, 14));
				registers[c.gridy].setMinimumSize(new Dimension(100, 20));
			}
			this.add(regs, BorderLayout.SOUTH);
			for (int i = 0; i < registers.length; i++) {
				registers[i].setEditable(false);
				registers[i].setBackground(Color.WHITE);
			}
		}
		
		public void update(int newSchwap) {
			schwap = newSchwap;
			schwapLabel.setText(getSwapString());
			for (int i = 0; i < registers.length; i++) {
				registers[i].setText(Integer.toHexString(emu.getSchwapRegister((short) this.schwap, (short) i)));
			}
		}

		private String getSwapString() {
			return (String.format("Schwap #%02d",this.schwap) + ((this.schwap == emu.getActiveSchwap())?"*":""));
		}
	}
	
	private class RunEmulatorTask extends SwingWorker<Void, Void> {
        @Override
        protected Void doInBackground() {
            while (!isCancelled()) {
            	if (emu.step()) {
                    update();
                    break;
            	}
            	update();
            }
            task = null;
            return null;
        }
    }
	
	class ConsoleStream implements Appendable {
				
		@Override
		public Appendable append(CharSequence arg0) throws IOException {
			console.append(arg0.toString() + "\n");
			System.out.println(arg0.toString());
			scroll.getVerticalScrollBar().setValue(scroll.getVerticalScrollBar().getMaximum());
			return this;
		}

		@Override
		public Appendable append(char arg0) throws IOException {
			console.append(new StringBuilder(arg0).toString());
			return this;
		}

		@Override
		public Appendable append(CharSequence arg0, int arg1, int arg2) throws IOException {
			return this.append(arg0);
		}
	}
	
	private class IlluminatiWindowListener implements WindowListener {
			JFrame dank_memes;
			Image i = null;
			SpinIlluminati spin;
			double angle = 0;
			final double angle_delta = Math.PI / 50.0;
			public IlluminatiWindowListener() {
				try {
					i = ImageIO.read(new File("IMG_0209.jpg"));
					i = i.getScaledInstance(600, 600, Image.SCALE_SMOOTH);
				}
				catch (IOException exc) {
				    exc.printStackTrace();
				}
				dank_memes = new JFrame("MICAH TAYLOR IS ILLUMINATI CONFIRMED"){
					private static final long serialVersionUID = 1L;

					@Override
					public void paint(Graphics g) {
						Graphics2D g2d = (Graphics2D) g;
						g2d.rotate(angle, 300, 300);
						g2d.drawImage(i, 0, 0, 600, 600, this);
						System.out.println(angle);
						angle += angle_delta;
					}
				};
				dank_memes.setSize(500,500);
				dank_memes.setResizable(false);
				dank_memes.setVisible(false);
				dank_memes.setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
				
			}
			public void windowActivated(WindowEvent arg0) {}
			public void windowClosed(WindowEvent arg0) {}
			public void windowClosing(WindowEvent arg0) {}
			public void windowDeactivated(WindowEvent arg0) {}
			public void windowDeiconified(WindowEvent arg0) {
				try {
					dank_memes.setVisible(true);
					dank_memes.repaint();
					AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(new File("spooky.wav").getAbsoluteFile());
					Clip clip = AudioSystem.getClip();
					clip.open(audioInputStream);
					FloatControl gainControl = 
						    (FloatControl) clip.getControl(FloatControl.Type.MASTER_GAIN);
					gainControl.setValue(6.0206f);
					gainControl.setValue(gainControl.getMaximum());
					clip.start();
					spin = new SpinIlluminati();
					new Thread(spin).start();
					new Thread(new RemoveIlluminati()).start();
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
			public void windowIconified(WindowEvent arg0) {}
			public void windowOpened(WindowEvent arg0) {}
			private class SpinIlluminati implements Runnable {
				boolean stop = false;
				@Override
				public void run() {
					try {
						while (!stop) {
							angle += angle_delta;
							dank_memes.repaint();
							Thread.sleep(20);
						}
					} catch (InterruptedException e) {
						e.printStackTrace();
						dank_memes.setVisible(false);
					}
				}
			}
			private class RemoveIlluminati implements Runnable {
				@Override
				public void run() {
					try {
						Thread.sleep(15000);
						dank_memes.setVisible(false);
						spin.stop = true;
					} catch (InterruptedException e) {
						e.printStackTrace();
						dank_memes.setVisible(false);
					}
				}
			}
	}
}



enum RegisterName {
	$0,
	$a0,
	$a1,
	$pc,
	$sp,
	$ra,
	$s0,
	$s1,
	$t0,
	$t1,
	$t2,
	$t3;
}