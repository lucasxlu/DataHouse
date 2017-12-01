SELECT
	TRUNCATE (
		(
			(
				substring_index(
					SUBSTR(
						jobsalaryname,
						1,
						instr(
							b.jobsalaryname,
							preprocess (b.jobsalaryname)
						) - 1
					),
					'-',
					1
				) + substring_index(
					SUBSTR(
						jobsalaryname,
						1,
						instr(
							b.jobsalaryname,
							preprocess (b.jobsalaryname)
						) - 1
					),
					'-',
					- (1)
				)
			) / (2 * u.model)
		) * u.ratio,
		2
	) avgsalary,
	b.*, u.*
FROM
	51job b
LEFT JOIN unit_convert u ON preprocess (b.jobsalaryname) = u.unit
