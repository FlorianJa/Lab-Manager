# from django.test import TestCase

# from lab_manager.models import FabLabUser,Material,Printer,Operating,UsageData

# # Unit tests for Models

# class FabLabUserModel(TestCase):
#     def setUp(self):
#         self.user = FabLabUser(rfid_uuid="1", username="user1",name="user1",is_login=True)
#         self.user.save()

#     def test_user_creation(self):
#         self.assertEqual(FabLabUser.objects.count(), 1)

#     def test_user_representation(self):
#         self.assertEqual(self.user.username,str(self.user.username))
#         self.assertEqual(self.user.name,str(self.user.name))
#         self.assertEqual(self.user.is_login,self.user.is_login)


# class MaterialModel(TestCase):
#     def setUp(self):
#         self.material = Material(filament_price=1.2, filament_weight=2.5,model_weight=3.4)
#         self.material.save()

#     def test_material_creation(self):
#         self.assertEqual(Material.objects.count(), 1)

# class OperatingModel(TestCase):
#     def setUp(self):
#         self.operating = Operating(power_consumption=2.6,electricity_cost=3.1)
#         self.operating.save()

#     def test_operating_creation(self):
#         self.assertEqual(Operating.objects.count(), 1)

# class PrinterModel(TestCase):
#     def setUp(self):
#         self.printer = Printer(price_printer=1000, lifespan=500,maintainence_cost=0.6)
#         self.printer.save()

#     def test_printer_creation(self):
#         self.assertEqual(Printer.objects.count(), 1)


# class UsageDataModel(TestCase):
#     def setUp(self):
#         self.usage = UsageData(owner="fablab", file_name="xyz.gcode",print_time=9187.03,time_stamp=1601410415,print_status="Done",printer_name="EOS",filament_price=1.2, filament_weight=2.5,model_weight=3.4,power_consumption=2.6,electricity_cost=3.1,price_printer=1000, lifespan=500,maintainence_cost=0.6)
#         self.usage.save()

#     def test_user_creation(self):
#         self.assertEqual(UsageData.objects.count(), 1)