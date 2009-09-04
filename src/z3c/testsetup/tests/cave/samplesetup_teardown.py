import z3c.testsetup
test_suite = z3c.testsetup.register_all_tests(
    'z3c.testsetup.tests.cave',
    zcml_config='sampleftesting.zcml',
    layer_name = 'SampleLayer',
    allow_teardown=False)
