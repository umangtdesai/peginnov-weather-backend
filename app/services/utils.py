# FUTURE: I ended up doing this on the frontend, and descoped this option for now. This class isn't used anywhere.
class Utils:
    '''
        Although the weather api gives us the ability to change units, we should maintain consistency in the DB. 
        This class handles the purely presentational concern of showing the data as either C or F since K isn't really understandble 
    '''

    @staticmethod
    def convert_kelvin_temperature(kelvin_temp, scale='C'):
        if scale.upper() == 'C':
            return Utils._kelvin_to_celsius(kelvin_temp)
        elif scale.upper() == 'F':
            return Utils._kelvin_to_fahrenheit(kelvin_temp)
        else:
            raise ValueError("Invalid scale. Please specify 'C' for Celsius or 'F' for Fahrenheit.")
        

    @staticmethod
    def _kelvin_to_celsius(kelvin_temp):
        celsius_temp = kelvin_temp - 273.15
        return celsius_temp

    @staticmethod
    def _kelvin_to_fahrenheit(kelvin_temp):
        celsius_temp = Utils.kelvin_to_celsius(kelvin_temp)
        fahrenheit_temp = (celsius_temp * 9/5) + 32
        return fahrenheit_temp
