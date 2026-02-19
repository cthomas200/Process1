
#Chyna Thomas

#Boundary Values
Max32 = 2**31 - 1
Min32 = -2**31

def decTobin(decimal):
    bit32 = decimal & 0xFFFFFFFF #AND operation to mask to 32 bits
    return f'{bit32:032b}' 

def binTohex(binary):
     value = int(binary, 2) 
     return f'0x{value:08x}' 

def binTodec(binary):
    value = int(binary, 2)
    if value >= 2**31: # if Most significant bit is 1 , the number is negative in 2's complement
        value -= 2**32 #subtract to get correct neg value
    return value

def checkoverflow(input):
  value = int(input)

  overflow = 0
  saturation = 0

  if value > Max32:
    overflow = 1
    saturation = 1
    value = Max32 #clamp to max
  elif value < Min32:
    overflow = 1
    saturation = 1
    value = Min32 #clamp to min
  return value, overflow, saturation

def main():
    int_value = input("Enter a 32-bit signed decimal: ").strip()
    try:
        value, overflow, saturation = checkoverflow(int_value)
    except ValueError:
        print("Invalid Input, Please enter a signed decimal integer")
        return


    output_fmt = input("Specify output format (BIN, DEC, HEX): ").strip().upper()
    binstr = decTobin(value) #convert everything to 32bit
    try:
        if output_fmt == "BIN":
            print(f'Output: {binstr}')
            print(f'overflow: {overflow}')
            print(f'saturation: {saturation}')
        elif output_fmt == "DEC":
            print(f'Output: {binTodec(binstr)}')
            print(f'overflow: {overflow}')
            print(f'saturation: {saturation}')
        elif output_fmt == "HEX":
            print(f'Output: {binTohex(binstr)}')
            print(f'overflow: {overflow}')
            print(f'saturation: {saturation}')
    except ValueError:
            print('Unknown format. Please enter DEC, BIN, HEX.')
    
    if overflow:
        min_or_max = "above max boundary" if int(int_value) > Max32 else "below min boundary"
        print(f'Input {int_value} is {min_or_max}. Value saturated to {value}')

main()