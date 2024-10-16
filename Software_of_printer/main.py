from timer_v1 import check_gcode_buffer
from timer_v1 import gcode_to_csv as gtc
from energy_estimation import get_energy

in_gcode_file = "1h03m_axle_bracket_orig.gcode"
out_gcode_file = "name_output.gcode"
csv_file = "coord_with_infos.csv"
nrg_csv_file = "coord_with_energy_consumption.csv"

check_gcode_buffer.main(in_gcode_file, out_gcode_file)

gtc.gcode_into_csv(out_gcode_file, csv_file)

get_energy.add_nrg_comsumption(csv_file, nrg_csv_file)