package edu.rose_hulman.csse232.groupM;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;

import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JSeparator;
import javax.swing.JSplitPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;

public class MainFrame extends JFrame {
	private static final long serialVersionUID = -5979979493835436236L;
	
	public static final short DEFAULT_SP = (short) 0xfff0;
	public static final short DEFAULT_PC = (short) 0x1000;
	
	private Emulator emu;
	
	private JTextArea console;
	private JTextArea instructionMem;
	private JTextArea dataMem;
	private StaticRegisterPanel staticRegs;
	private SchwapPanel schwapRegs;
	
	public MainFrame() {
		super("JSchpim");
		MainFrame selfRef = this;
		emu = new Emulator(DEFAULT_SP, DEFAULT_PC);
		this.setLayout(new BorderLayout());
		JPanel buttonsPanel = new JPanel();
		JButton reset = new JButton("Reset");
		reset.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent arg0) {
				emu.write("Reset emulator!");
				emu.setRegister((short) 3, DEFAULT_PC);
				emu.setRegister((short) 4, DEFAULT_SP);
				emu.mem.clear();
				selfRef.update();
			}
		});
		buttonsPanel.add(reset);
		JButton load = new JButton("Load");
		load.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				JFileChooser chooser = new JFileChooser();
			    int returnVal = chooser.showOpenDialog(selfRef);
			    if(returnVal == JFileChooser.APPROVE_OPTION) {
			    	emu.write("Loading assembly file: " +
			            chooser.getSelectedFile().getName());
			       	try {
						Scanner sc = new Scanner(chooser.getSelectedFile());
						ArrayList<String> al = new ArrayList<String>();
						al.add("#" + Integer.toHexString(MainFrame.DEFAULT_PC));
						while (sc.hasNextLine())
							al.add(sc.nextLine());
						String[] arr = new String[0];
						arr = al.toArray(arr);
						sc.close();
						emu.loadDataMemory(arr);
						selfRef.update();
					} catch (FileNotFoundException e1) {
						e1.printStackTrace();
						emu.write(e1.getMessage());
					}
			    }
			    
			}
		});
		JButton step = new JButton("Step");
		step.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				emu.step();
				selfRef.update();
			}
		});
		buttonsPanel.add(load);
		buttonsPanel.add(step);
		this.add(buttonsPanel, BorderLayout.NORTH);
		JSplitPane main = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT);
		JPanel registerPanel = new JPanel(new BorderLayout());
		registerPanel.add(staticRegs = new StaticRegisterPanel(), BorderLayout.NORTH);
		registerPanel.add(schwapRegs = new SchwapPanel(), BorderLayout.CENTER);
		main.add(registerPanel);
		JSplitPane leftPanel = new JSplitPane(JSplitPane.VERTICAL_SPLIT);
		leftPanel.add(console = new JTextArea());
		JSplitPane mem = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT);
		mem.add(instructionMem = new JTextArea());
		mem.add(dataMem = new JTextArea());		
		leftPanel.add(mem);
		main.add(leftPanel);
		console.setEditable(false);
		console.setPreferredSize(new Dimension(600, 200));
		console.setForeground(Color.RED);
		emu.setConsoleStream(new ConsoleStream(console));
		instructionMem.setEditable(false);
		instructionMem.setPreferredSize(new Dimension(200, 100));
		dataMem.setEditable(false);
		this.add(main, BorderLayout.CENTER);
		update();
		this.pack();
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		this.setVisible(true);
		emu.write("Initialized emulator @ $SP=%04x, $PC=%04x", emu.getRegister((short) 4), emu.getRegister((short) 3));
		emu.write("NOTE: Currently the scroll bar doesn't work/exist. This will be fixed.");
		emu.write("For **magical** reasons, a \"not\" with an immediate does not work (yet).");
		emu.write("In the machine code file you load, 1 instruction per line in form 0x[Hex value]");
		emu.write("Empty lines are bad.");
		emu.write("If you don't, it will freak out and probably not work.");
		emu.write("Syscall 10 => print schwap. Syscall 0 ==> exit (not yet impl)");
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
			for (c.gridy = 0; c.gridy < names.length; c.gridy++) {
				c.gridx = 0;
				c.weightx = 0.5;
				c.anchor = GridBagConstraints.LINE_START;
				c.fill = GridBagConstraints.NONE;
				this.add(new JLabel(names[c.gridy].name()), c);
				c.gridx = 1;
				c.weightx = 1;
				c.anchor = GridBagConstraints.LINE_END;
				c.fill = GridBagConstraints.HORIZONTAL;
				this.add(registers[c.gridy] = new JTextField(Integer.toHexString(emu.getRegister((short) c.gridy))), c); 
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

		private int schwap;
		private static final int schwapMod = 15;
		
		private JLabel schwapLabel;
		
		private JTextField[] registers;
		
		public SchwapPanel() {
			super(new BorderLayout());
			schwap = 0;
			registers = new JTextField[4];
			JPanel top = new JPanel(new BorderLayout());
			top.add(new JSeparator(), BorderLayout.NORTH);
			JButton l = new JButton("<");
			l.addActionListener(new ActionListener(){
				@Override
				public void actionPerformed(ActionEvent arg0) {
					schwap = ((schwap - 1) + schwapMod) % schwapMod;
					update(schwap);
				}
			});
			JButton r = new JButton(">");
			r.addActionListener(new ActionListener(){
				@Override
				public void actionPerformed(ActionEvent arg0) {
					schwap = ((schwap + 1)) % schwapMod;
					update(schwap);
				}
			});
			top.add(l, BorderLayout.WEST);
			top.add(r, BorderLayout.EAST);
			top.add(schwapLabel = new JLabel(getSwapString()), BorderLayout.CENTER);
			this.add(top, BorderLayout.NORTH);
			JPanel regs = new JPanel(new GridBagLayout());
			GridBagConstraints c = new GridBagConstraints();
			for (c.gridy = 0; c.gridy < 4; c.gridy++) {
				c.gridx = 0;
				c.weightx = 0.5;
				c.anchor = GridBagConstraints.LINE_START;
				c.fill = GridBagConstraints.NONE;
				regs.add(new JLabel("$h" + c.gridy), c);
				c.gridx = 1;
				c.weightx = 1;
				c.anchor = GridBagConstraints.LINE_END;
				c.fill = GridBagConstraints.HORIZONTAL;
				regs.add(registers[c.gridy] = new JTextField(Integer.toHexString(emu.getSchwapRegister((short) schwap,(short) c.gridy))), c);
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
	
	class ConsoleStream implements Appendable {

		private JTextArea console;
		
		public ConsoleStream(JTextArea con) {
			console = con;
		}
		
		@Override
		public Appendable append(CharSequence arg0) throws IOException {
			console.append(arg0.toString() + "\n");
			System.out.println(arg0.toString());
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