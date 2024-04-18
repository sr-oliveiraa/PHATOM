from PIL import Image

class SteganographyFramework:
    def hide_code_in_image(self, image_path, code, output_path):
        img = Image.open(image_path)
        width, height = img.size
        code_binary = ''.join(format(ord(char), '08b') for char in code) + '1111111111111110' # Adiciona um delimitador de fim de mensagem
        code_length = len(code_binary)
        pixel_index = 0

        for y in range(height):
            for x in range(width):
                if pixel_index < code_length:
                    pixel = list(img.getpixel((x, y)))
                    for i in range(3): # Percorre os canais RGB da imagem
                        if pixel[i] % 2 == 0 and int(code_binary[pixel_index]) == 1:
                            pixel[i] += 1
                        elif pixel[i] % 2 == 1 and int(code_binary[pixel_index]) == 0:
                            pixel[i] -= 1
                        pixel_index += 1
                        if pixel_index >= code_length:
                            break
                    img.putpixel((x, y), tuple(pixel))
                else:
                    break
            else:
                continue
            break

        img.save(output_path)

    def extract_code_from_image(self, image_path):
        img = Image.open(image_path)
        width, height = img.size
        binary = ''
        for y in range(height):
            for x in range(width):
                pixel = img.getpixel((x, y))
                for i in range(3):
                    binary += str(pixel[i] % 2)
        delimiter_index = binary.find('1111111111111110')
        binary = binary[:delimiter_index]
        code = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
        return code

# Exemplo de uso

framework = SteganographyFramework()

# Solicitação de entrada do usuário
image_path = input("Digite o caminho da imagem: ")
output_path = input("Digite o caminho de saída da imagem oculta: ")
code = input("Digite o código a ser ocultado na imagem: ")

# Oculta o código na imagem
framework.hide_code_in_image(image_path, code, output_path)
print("Código oculto na imagem com sucesso!")

# Extraindo o código oculto da imagem
extracted_code = framework.extract_code_from_image(output_path)
print("Código extraído da imagem:")
print(extracted_code)

# Avaliando o código extraído
try:
    exec(extracted_code)
except Exception as e:
    print("Erro ao executar o código extraído:", e)
