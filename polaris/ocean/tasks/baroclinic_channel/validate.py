from polaris import Step
from polaris.validate import compare_variables


class Validate(Step):
    """
    A step for comparing outputs between steps in a baroclinic channel run

    Attributes
    ----------
    step_subdirs : list of str
        The number of processors used in each run
    """
    def __init__(self, task, step_subdirs):
        """
        Create the step

        Parameters
        ----------
        task : polaris.Task
            The task this step belongs to

        step_subdirs : list of str
            The number of processors used in each run
        """
        super().__init__(task=task, name='validate')

        self.step_subdirs = step_subdirs

        for subdir in step_subdirs:
            self.add_input_file(filename=f'output_{subdir}.nc',
                                target=f'../{subdir}/output.nc')

    def run(self):
        """
        Compare ``temperature``, ``salinity``, ``layerThickness`` and
        ``normalVelocity`` in the outputs of two previous steps with each other
        """
        super().run()
        step_subdirs = self.step_subdirs
        variables = ['temperature', 'salinity', 'layerThickness',
                     'normalVelocity']
        all_pass = compare_variables(variables=variables,
                                     filename1=self.inputs[0],
                                     filename2=self.inputs[1],
                                     logger=self.logger)
        if not all_pass:
            raise ValueError(f'Validation failed comparing outputs between '
                             f'{step_subdirs[0]} and {step_subdirs[1]}.')
