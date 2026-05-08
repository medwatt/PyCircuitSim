import pytest
from pycircuitsim.netlisting import Circuit, SubCircuit
from pycircuitsim.netlisting.components.passive import (
    Resistor, Inductor, Capacitor,
    MutualInductance, VoltageControlledSwitch, CurrentControlledSwitch,
    LosslessTransmissionLine,
)
from pycircuitsim.netlisting.components.semiconductors import Diode, JFET, Mosfet, BJT
from pycircuitsim.netlisting.components.independent import (
    VoltageSource, CurrentSource,
    VoltagePulse, CurrentPulse,
    VoltageSin, CurrentSin,
    VoltageExp, CurrentExp,
    VoltagePWL, CurrentPWL,
    VoltageTransientNoise, CurrentTransientNoise,
)
from pycircuitsim.netlisting.components.dependent import (
    VoltageControlledCurrentSource,
    VoltageControlledVoltageSource,
    CurrentControlledCurrentSource,
    CurrentControlledVoltageSource,
    BehavioralSource,
)
from pycircuitsim.netlisting.components.instance import SubCircuitInstance, OsdiInstance


# ─── Passive ─────────────────────────────────────────────────────────────────

class TestPassive:
    def test_resistor(self):
        assert str(Resistor("1", ("a", "b"), "1k")) == "R1 a b 1k"

    def test_resistor_params(self):
        assert str(Resistor("1", ("a", "b"), "1k", temp="25")) == "R1 a b 1k temp=25"

    def test_inductor(self):
        assert str(Inductor("1", ("a", "b"), "1u")) == "L1 a b 1u"

    def test_capacitor(self):
        assert str(Capacitor("1", ("a", "b"), "1n")) == "C1 a b 1n"

    def test_mutual_inductance(self):
        assert str(MutualInductance("1", "1", "2", "0.9")) == "K1 L1 L2 0.9"

    def test_mutual_inductance_tight_coupling(self):
        assert str(MutualInductance("xfmr", "a", "b", "1")) == "Kxfmr La Lb 1"

    def test_voltage_controlled_switch(self):
        assert str(VoltageControlledSwitch("1", ("n1", "n2", "nc1", "nc2"), "MYSW")) == "S1 n1 n2 nc1 nc2 MYSW"

    def test_voltage_controlled_switch_initial_state(self):
        assert str(VoltageControlledSwitch("1", ("n1", "n2", "nc1", "nc2"), "MYSW", "off")) == "S1 n1 n2 nc1 nc2 MYSW off"

    def test_current_controlled_switch(self):
        assert str(CurrentControlledSwitch("1", ("n1", "n2"), "Vctrl", "MYSW")) == "W1 n1 n2 Vctrl MYSW"

    def test_current_controlled_switch_initial_state(self):
        assert str(CurrentControlledSwitch("1", ("n1", "n2"), "Vctrl", "MYSW", "on")) == "W1 n1 n2 Vctrl MYSW on"

    def test_transmission_line_td(self):
        assert str(LosslessTransmissionLine("1", ("in", "0", "out", "0"), "50", td="1ns")) == "T1 in 0 out 0 Z0=50 TD=1ns"

    def test_transmission_line_frequency(self):
        assert str(LosslessTransmissionLine("1", ("in", "0", "out", "0"), "75", frequency="1e9")) == "T1 in 0 out 0 Z0=75 F=1e9 NL=0.25"

    def test_transmission_line_frequency_custom_nl(self):
        assert str(LosslessTransmissionLine("1", ("in", "0", "out", "0"), "75", frequency="1e9", nl="0.5")) == "T1 in 0 out 0 Z0=75 F=1e9 NL=0.5"

    def test_transmission_line_no_delay(self):
        assert str(LosslessTransmissionLine("1", ("in", "0", "out", "0"), "50")) == "T1 in 0 out 0 Z0=50"


# ─── Semiconductors ──────────────────────────────────────────────────────────

class TestSemiconductors:
    def test_diode(self):
        assert str(Diode("1", ("anode", "cathode"), "D1N4148")) == "D1 anode cathode D1N4148"

    def test_diode_params(self):
        assert str(Diode("1", ("a", "k"), "D1N4148", area="2")) == "D1 a k D1N4148 area=2"

    def test_jfet(self):
        assert str(JFET("1", ("d", "g", "s"), "NJFET")) == "J1 d g s NJFET"

    def test_jfet_area(self):
        assert str(JFET("1", ("d", "g", "s"), "NJFET", area="2.0")) == "J1 d g s NJFET 2.0"

    def test_jfet_params(self):
        assert str(JFET("1", ("d", "g", "s"), "NJFET", temp="27")) == "J1 d g s NJFET temp=27"

    def test_mosfet(self):
        assert str(Mosfet("1", ("d", "g", "s", "b"), "NMOS")) == "M1 d g s b NMOS"

    def test_mosfet_params(self):
        assert str(Mosfet("1", ("d", "g", "s", "b"), "NMOS", l="1u", w="10u")) == "M1 d g s b NMOS l=1u w=10u"

    def test_bjt(self):
        assert str(BJT("1", ("c", "b", "e"), "NPN")) == "Q1 c b e NPN"

    def test_bjt_ns(self):
        assert str(BJT("1", ("c", "b", "e"), "NPN", ns="1")) == "Q1 c b e 1 NPN"

    def test_bjt_params(self):
        assert str(BJT("1", ("c", "b", "e"), "NPN", temp="27")) == "Q1 c b e NPN temp=27"


# ─── Independent Sources ─────────────────────────────────────────────────────

class TestIndependentSources:
    def test_voltage_source_dc(self):
        assert str(VoltageSource("1", ("vdd", "0"), "1.8")) == "V1 vdd 0 DC 1.8"

    def test_voltage_source_ac(self):
        assert str(VoltageSource("1", ("in", "0"), "0", ac_magnitude="1")) == "V1 in 0 DC 0 AC 1 0"

    def test_voltage_source_ac_phase(self):
        assert str(VoltageSource("1", ("in", "0"), "0", ac_magnitude="1", ac_phase="90")) == "V1 in 0 DC 0 AC 1 90"

    def test_current_source_dc(self):
        assert str(CurrentSource("1", ("a", "b"), "1m")) == "I1 a b DC 1m"

    def test_voltage_pulse(self):
        assert str(VoltagePulse("1", ("a", "0"), "0", "1.8", period="10n", pulse_width="5n")) == "V1 a 0 PULSE(0 1.8 0 0 0 5n 10n)"

    def test_current_pulse(self):
        assert str(CurrentPulse("1", ("a", "0"), "0", "1m")) == "I1 a 0 PULSE(0 1m 0 0 0 0 0)"

    def test_voltage_sin(self):
        assert str(VoltageSin("1", ("a", "0"), "1", "1k")) == "V1 a 0 SIN(0 1 1k 0 0 0)"

    def test_voltage_sin_offset(self):
        assert str(VoltageSin("1", ("a", "0"), "1", "1k", offset="0.5")) == "V1 a 0 SIN(0.5 1 1k 0 0 0)"

    def test_current_sin(self):
        assert str(CurrentSin("1", ("a", "0"), "1m", "50k")) == "I1 a 0 SIN(0 1m 50k 0 0 0)"

    def test_voltage_exp(self):
        assert str(VoltageExp("1", ("a", "0"), "0", "1.8", rise_delay_time="1n", rise_time_constant="5n")) == "V1 a 0 EXP(0 1.8 1n 5n 0 0)"

    def test_current_exp(self):
        assert str(CurrentExp("1", ("a", "0"), "0", "1m")) == "I1 a 0 EXP(0 1m 0 0 0 0)"

    def test_voltage_pwl(self):
        assert str(VoltagePWL("1", ("a", "0"), [("0", "0"), ("1n", "1.8"), ("2n", "0")])) == "V1 a 0 PWL(0 0 1n 1.8 2n 0)"

    def test_voltage_pwl_repeat(self):
        assert str(VoltagePWL("1", ("a", "0"), [("0", "0"), ("1n", "1")], repeat_time="0")) == "V1 a 0 PWL(0 0 1n 1) r=0"

    def test_current_pwl(self):
        assert str(CurrentPWL("1", ("a", "0"), [("0", "0"), ("1n", "1m")])) == "I1 a 0 PWL(0 0 1n 1m)"

    def test_voltage_transient_noise(self):
        assert str(VoltageTransientNoise("1", ("a", "0"), rms_noise_amplitude="1m", time_step="1n")) == "V1 a 0 TRNOISE(1m 1n 0 0 0 0 0)"

    def test_current_transient_noise(self):
        assert str(CurrentTransientNoise("1", ("a", "0"))) == "I1 a 0 TRNOISE(0 0 0 0 0 0 0)"


# ─── Dependent Sources ───────────────────────────────────────────────────────

class TestDependentSources:
    def test_vccs(self):
        assert str(VoltageControlledCurrentSource("1", ("out", "0", "in", "0"), "0.01")) == "G1 out 0 in 0 0.01"

    def test_vcvs(self):
        assert str(VoltageControlledVoltageSource("1", ("out", "0", "in", "0"), "10")) == "E1 out 0 in 0 10"

    def test_cccs(self):
        assert str(CurrentControlledCurrentSource("1", ("out", "0", "in", "0"), "5")) == "F1 out 0 in 0 5"

    def test_ccvs(self):
        assert str(CurrentControlledVoltageSource("1", ("out", "0", "in", "0"), "100")) == "H1 out 0 in 0 100"

    def test_behavioral_voltage(self):
        assert str(BehavioralSource("1", ("out", "0"), voltage_expression="v(in)*2")) == "B1 out 0 v=v(in)*2"

    def test_behavioral_current(self):
        assert str(BehavioralSource("1", ("out", "0"), current_expression="i(Vsense)*3")) == "B1 out 0 i=i(Vsense)*3"

    def test_behavioral_requires_expression(self):
        with pytest.raises(ValueError):
            BehavioralSource("1", ("a", "0"))

    def test_behavioral_rejects_both_expressions(self):
        with pytest.raises(ValueError):
            BehavioralSource("1", ("a", "0"), current_expression="1", voltage_expression="1")


# ─── Instances ───────────────────────────────────────────────────────────────

class TestInstances:
    def test_subcircuit_instance(self):
        sub = SubCircuit("myfilter", ["in", "out"])
        assert str(SubCircuitInstance("1", ("a", "b"), sub)) == "X1 a b myfilter"

    def test_subcircuit_instance_params(self):
        sub = SubCircuit("myfilter", ["in", "out"])
        assert str(SubCircuitInstance("1", ("a", "b"), sub, params={"r": "1k"})) == "X1 a b myfilter r=1k"

    def test_subcircuit_instance_copy(self):
        sub = SubCircuit("myfilter", ["in", "out"])
        assert str(SubCircuitInstance("1", ("a", "b"), sub, copy=True)) == "X1 a b myfilter_1"

    def test_osdi_instance(self):
        assert str(OsdiInstance("1", ("a", "b", "c"), "mymodel")) == "N1 a b c mymodel"

    def test_osdi_instance_params(self):
        assert str(OsdiInstance("1", ("a", "b"), "mymodel", params={"w": "1u"})) == "N1 a b mymodel w=1u"


# ─── Circuit integration ─────────────────────────────────────────────────────

class TestCircuitIntegration:
    def test_duplicate_id_raises(self):
        c = Circuit()
        c.R("1", ("a", "b"), "1k")
        with pytest.raises(ValueError):
            c.R("1", ("c", "d"), "2k")

    def test_same_id_different_type_ok(self):
        c = Circuit()
        c.R("1", ("a", "b"), "1k")
        c.C("1", ("a", "b"), "1n")

    def test_netlist_order(self):
        c = Circuit("test")
        c.R("1", ("a", "b"), "1k")
        c.C("1", ("a", "b"), "1n")
        lines = c.get_netlist()
        assert lines[1] == "R1 a b 1k"
        assert lines[2] == "C1 a b 1n"

    def test_define_model(self):
        c = Circuit("test")
        c.define_model("NMOS", "NMOS", Kp="190u", Vto="0.57")
        assert ".model NMOS NMOS (Kp=190u Vto=0.57)" in c.get_netlist()

    def test_set_initial_conditions(self):
        c = Circuit("test")
        c.set_initial_conditions({"out": "0", "vdd": "1.8"})
        assert ".ic v(out)=0 v(vdd)=1.8" in c.get_netlist()

    def test_set_nodeset_all(self):
        c = Circuit("test")
        c.set_nodeset(all_value="0")
        assert ".nodeset all=0" in c.get_netlist()

    def test_set_nodeset_nodes(self):
        c = Circuit("test")
        c.set_nodeset(node_guesses={"vdd": "1.8"})
        assert ".nodeset v(vdd)=1.8" in c.get_netlist()

    def test_subcircuit_in_netlist(self):
        sub = SubCircuit("myfilter", ["in", "out"])
        sub.R("1", ("in", "out"), "1k")
        c = Circuit("test")
        c.X("1", ("a", "b"), subcircuit=sub)
        netlist = str(c)
        assert ".subckt myfilter in out" in netlist
        assert "R1 in out 1k" in netlist
        assert ".ends myfilter" in netlist
        assert "X1 a b myfilter" in netlist

    def test_include(self):
        c = Circuit("test")
        c.include("/path/to/models.sp")
        lines = c.get_netlist()
        assert '.include "/path/to/models.sp"' in lines
        assert lines.index('.include "/path/to/models.sp"') == 1

    def test_lib_no_section(self):
        c = Circuit("test")
        c.lib("/path/to/pdk.lib")
        assert '.lib "/path/to/pdk.lib"' in c.get_netlist()

    def test_lib_with_section(self):
        c = Circuit("test")
        c.lib("/path/to/pdk.lib", "tt")
        assert '.lib "/path/to/pdk.lib" tt' in c.get_netlist()

    def test_include_before_components(self):
        c = Circuit("test")
        c.include("/path/to/models.sp")
        c.R("1", ("a", "b"), "1k")
        lines = c.get_netlist()
        assert lines.index('.include "/path/to/models.sp"') < lines.index("R1 a b 1k")

    def test_include_preserves_path_case(self):
        c = Circuit("test")
        c.include("/path/To/Models.sp")
        assert '.include "/path/To/Models.sp"' in c.get_netlist()

    def test_param(self):
        c = Circuit("test")
        c.param(Rval="1k", Cval="100n")
        assert ".param Rval=1k Cval=100n" in c.get_netlist()

    def test_param_before_components(self):
        c = Circuit("test")
        c.param(Rval="1k")
        c.R("1", ("a", "b"), "{Rval}")
        lines = c.get_netlist()
        assert lines.index(".param Rval=1k") < lines.index("R1 a b {Rval}")

    def test_param_in_subcircuit(self):
        sub = SubCircuit("myfilter", ["in", "out"])
        sub.param(Rval="1k")
        sub.R("1", ("in", "out"), "{Rval}")
        c = Circuit("test")
        c.X("1", ("a", "b"), subcircuit=sub)
        netlist = str(c)
        assert ".param Rval=1k" in netlist
        subckt_start = netlist.index(".subckt myfilter")
        subckt_end = netlist.index(".ends myfilter")
        param_pos = netlist.index(".param Rval=1k")
        assert subckt_start < param_pos < subckt_end

    def test_new_components_in_netlist(self):
        c = Circuit("test")
        c.L("1", ("a", "b"), "1u")
        c.L("2", ("c", "d"), "2u")
        c.K("1", "1", "2", "0.9")
        c.J("1", ("d", "g", "s"), "NJFET")
        c.S("1", ("n1", "n2", "nc1", "nc2"), "SW")
        c.W("1", ("n1", "n2"), "Vctrl", "SW")
        c.T("1", ("in", "0", "out", "0"), "50", td="1ns")
        lines = c.get_netlist()
        assert "K1 L1 L2 0.9" in lines
        assert "J1 d g s NJFET" in lines
        assert "S1 n1 n2 nc1 nc2 SW" in lines
        assert "W1 n1 n2 Vctrl SW" in lines
        assert "T1 in 0 out 0 Z0=50 TD=1ns" in lines
