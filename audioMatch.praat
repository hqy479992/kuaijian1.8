form Cross Correlate two Sounds
    sentence input_sound_1
    sentence input_sound_2
    sentence filename
    real start_time 0
    real end_time 1800
endform
form Extract_and_save_intervals
	comment Select the Sound you want to extract the intervals from
	comment
	comment Do you want to extract all interval?
	comment If you don`t write here the label of the intervals you don`t want to extract.
	word do_not_extract x
	comment If you do not want to extract empty intervals write ""

	word prefix wl07
	word suffix 1
endform
form Extract_and_save_intervals
	comment Select the Sound you want to extract the intervals from
	comment
	comment Do you want to extract all interval?
	comment If you don`t write here the label of the intervals you don`t want to extract.
	word do_not_extract x
	comment If you do not want to extract empty intervals write ""

	word prefix wl07
	word suffix 1
endform

procedure extract_and_save_intervals: .directoryOutput$
	#.directoryOutput$ = chooseDirectory$: "Choose a directory to save all the new files in"
	if .directoryOutput$ <> ""
		.numberOfSelectedSounds = numberOfSelected ("Sound")
		if .numberOfSelectedSounds = 0
		pause Select the Sound you want to extract from and click OK
		endif
		.base$ = selected$ ("Sound")
		selectObject: "TextGrid " + .base$

		#compruebo que el grid sea de ese Sound
		.soundDur = Get total duration
		.gridDur = Get total duration
		if .soundDur<>.gridDur
			El sonido y el TextGrid tienen duraciones diferentes. Â¿Seguro que son del mismo archivo?
		endif

		#me apetecia que el margen de los archivos fuera silencio puro, pero para limpiarlos no irÃ¡ bien...
		#selectObject: "Sound " + .base$
		# sampl_frequ = Get sampling frequency
		# silence = Create Sound from formula: "silence", 1, 0, 0.2, sampl_frequ, "0"
		# silence2 = Create Sound from formula: "silence", 1, 0, 0.2, sampl_frequ, "0"
		.numberOfIntervals = Get number of intervals: 1
		for .interval from 1 to .numberOfIntervals

			selectObject: "TextGrid " + .base$
			.codigo$ = Get label of interval: 1, .interval
			if .codigo$ <> marca_de_silencio$
			echo Extrayendo intervalo '.interval' '.codigo$'
				.int_start = Get start point: 1, .interval
				.int_end = Get end point: 1, .interval
				selectObject: "Sound " +.base$
				#extraigo los intervalos con un margen porque sino van muy justos, en el caso de que sea el primer sonido o el ÃƒÂºltimo no hay posibilidad de silencio
				if .interval = 1
					Extract part: .int_start, .int_end+0.2, "rectangular", 1, 0
				elif .interval = .numberOfIntervals
					Extract part: .int_start-0.2, .int_end, "rectangular", 1, 0
				else
					Extract part: .int_start-0.2, .int_end+0.2, "rectangular", 1, 0
				endif
				Save as WAV file: .directoryOutput$ + "/" + informante$ + .codigo$ + repeticion$ +  ".wav"
				Remove
			endif
		endfor
	endif
endproc

Open long sound file... 'input_sound_1$'
Extract part: 0, 1800, "no"
Extract one channel... 1
sound1 = selected("Sound")
Open long sound file... 'input_sound_2$'
Extract part: 0, 1800, "no"
Extract one channel... 1
sound2 = selected("Sound")
procedure extract_and_save_intervals: .directoryOutput$
	#.directoryOutput$ = chooseDirectory$: "Choose a directory to save all the new files in"
	if .directoryOutput$ <> ""
		.numberOfSelectedSounds = numberOfSelected ("Sound")
		if .numberOfSelectedSounds = 0
		pause Select the Sound you want to extract from and click OK
		endif
		.base$ = selected$ ("Sound")
		selectObject: "TextGrid " + .base$

		#compruebo que el grid sea de ese Sound
		.soundDur = Get total duration
		.gridDur = Get total duration
		if .soundDur<>.gridDur
			El sonido y el TextGrid tienen duraciones diferentes. Â¿Seguro que son del mismo archivo?
		endif

		#me apetecia que el margen de los archivos fuera silencio puro, pero para limpiarlos no irÃ¡ bien...
		#selectObject: "Sound " + .base$
		# sampl_frequ = Get sampling frequency
		# silence = Create Sound from formula: "silence", 1, 0, 0.2, sampl_frequ, "0"
		# silence2 = Create Sound from formula: "silence", 1, 0, 0.2, sampl_frequ, "0"
		.numberOfIntervals = Get number of intervals: 1
		for .interval from 1 to .numberOfIntervals

			selectObject: "TextGrid " + .base$
			.codigo$ = Get label of interval: 1, .interval
			if .codigo$ <> marca_de_silencio$
			echo Extrayendo intervalo '.interval' '.codigo$'
				.int_start = Get start point: 1, .interval
				.int_end = Get end point: 1, .interval
				selectObject: "Sound " +.base$
				#extraigo los intervalos con un margen porque sino van muy justos, en el caso de que sea el primer sonido o el ÃƒÂºltimo no hay posibilidad de silencio
				if .interval = 1
					Extract part: .int_start, .int_end+0.2, "rectangular", 1, 0
				elif .interval = .numberOfIntervals
					Extract part: .int_start-0.2, .int_end, "rectangular", 1, 0
				else
					Extract part: .int_start-0.2, .int_end+0.2, "rectangular", 1, 0
				endif
				Save as WAV file: .directoryOutput$ + "/" + informante$ + .codigo$ + repeticion$ +  ".wav"
				Remove
			endif
		endfor
	endif
endproc
select sound1
plus sound2
Cross-correlate: "peak 0.99", "zero"
offset = Get time of maximum: 0,0, "Sinc70"
procedure fric_analysis
	appendFile ("'txtName$'.txt", "'speakersId$'	", "'base$'	", "'intervalLabel$'	")
	#saca donde empieza el intervalo
	.intervalStart = Get start point: 1, n
	.intervalEnd = Get end point: 1, n
	.intervalDur = .intervalEnd - .intervalStart
	.intervalStartms = .intervalStart*1000
	.intervalEndms= .intervalEnd*1000
	.intervalDurms = .intervalDur*1000
	.intervalStartms$ = fixed$ (.intervalStartms, 0)
	.intervalEndms$ = fixed$ (.intervalEndms, 0)
	.intervalDurms$ = fixed$ (.intervalDurms, 0)



	select LongSound 'base$'
	#si el intervalo es menor de 0-030 el valor 2 = intervalEnd
	.targetEnd = .intervalStart + 0.030
	if .targetEnd > .intervalEnd
		.targetEnd = .intervalEnd
	endif
	printline '.intervalStart' - '.intervalEnd' targetEnd: '.targetEnd'

	select LongSound 'base$'
	Extract part: .intervalStart, .targetEnd, "yes"
	To PointProcess (zeroes): 1, "yes", "yes"
	.numeroDePuntos = Get number of points
	Remove

	select LongSound 'base$'
	Extract part: .intervalStart, .intervalEnd, "yes"
	Rename: "fricative"
	To PointProcess (zeroes): 1, "yes", "yes"
	.numeroPuntosIntervalo = Get number of points
	.zCrossing = (.numeroPuntosIntervalo*10) / .intervalDurms
	.zCrossing$ = fixed$ (.zCrossing, 2)
	#appendFile ("'txtName$'.txt", "'intervalStart'	", "'intervalEnd'	", "'intervalDur'", "'numeroDePuntos'	", 'newline$')
	appendFile: txtNameExtension$, .intervalStartms$, tab$, .intervalEndms$, tab$, .intervalDurms$, tab$, .numeroDePuntos, tab$, .numeroPuntosIntervalo, tab$, .zCrossing$, tab$


	# MOMENTOS ESPECTRALES
	select Sound fricative
	# Using a filter is a suggestion by Ricard Herrero and Daniel Recasens
	if filter = 1
		Filter (pass Hann band): 1000, 11000, 100
	endif

	To Ltas: 150
	.max_freq = Get frequency of maximum: 0, 0, "Cubic"
	.max_freq$ = fixed$ (.max_freq, 0)
	appendFile: txtNameExtension$, .max_freq$, tab$

	select Sound fricative
	To Intensity: 500, 0, "yes"
	.min_intensity = Get minimum: 0, 0, "Parabolic"
	.max_intensity = Get maximum: 0, 0, "Parabolic"
	.mean_intensity = Get mean: 0, 0, "energy"

	.min_intensity$ = fixed$ (.min_intensity, 0)
	.max_intensity$ = fixed$ (.max_intensity, 0)
	.mean_intensity$ = fixed$ (.mean_intensity, 0)
	appendFile: txtNameExtension$, .min_intensity$, tab$, .max_intensity$, tab$, .mean_intensity$, tab$

	select Sound fricative
	To Spectrum: "yes"
	.center_gravity = Get centre of gravity: 2
	.skewness = Get skewness: 2
	.kurtosis = Get kurtosis: 2
	.standard_dev = Get standard deviation: 2
	.central_moment = Get central moment: 3, 2

	.center_gravity$ = fixed$ (.center_gravity, 4)
	.skewness$ = fixed$ (.skewness, 4)
	.kurtosis$ = fixed$(.kurtosis, 4)
	.standard_dev$ = fixed$ (.standard_dev, 4)
	.central_moment$ = fixed$ (.central_moment, 4)
	appendFile: txtNameExtension$, .center_gravity$, tab$, .skewness$, tab$, .kurtosis$, tab$, .standard_dev$, tab$, .central_moment$, newline$
	#limpia de la lista de objetos
	select Sound fricative
	Remove
endproc
writeInfoLine: 'offset'
appendFileLine: filename$, input_sound_1$, "_", input_sound_2$, "_", offset

