import pygame
import argparse

def process_spritesheet(input_path, output_path, line_index, num_lines, num_columns):
    pygame.init()
    line_index -= 1
    spritesheet = pygame.image.load(input_path)
    width, height = spritesheet.get_size()

    frame_height = height // num_lines
    frame_width = width // num_columns

    new_spritesheet = pygame.Surface((width, height + frame_height), pygame.SRCALPHA)  # Augmente la hauteur pour ajouter la nouvelle ligne

    new_spritesheet.blit(spritesheet, (0, 0))

    for i in range(num_columns):
        frame = spritesheet.subsurface((i * frame_width, line_index * frame_height, frame_width, frame_height))
        inverted_frame = pygame.transform.flip(frame, True, False)
        new_spritesheet.blit(inverted_frame, (i * frame_width, height))  # Colle sous l'original

    pygame.image.save(new_spritesheet, output_path)
    print(f"Spritesheet modifié sauvegardé à : {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Inverser une ligne d'un spritesheet et ajouter la ligne inversée.")
    
    parser.add_argument("input_path", help="Chemin vers le spritesheet original")
    parser.add_argument("output_path", help="Chemin vers le spritesheet modifié")
    parser.add_argument("line_index", type=int, help="Numéro de la ligne à inverser (commence à 0)")
    parser.add_argument("num_lines", type=int, help="Nombre total de lignes dans le spritesheet")
    parser.add_argument("num_columns", type=int, help="Nombre total de colonnes dans le spritesheet")
    
    args = parser.parse_args()

    process_spritesheet(args.input_path, args.output_path, args.line_index, args.num_lines, args.num_columns)

if __name__ == "__main__":
    main()
