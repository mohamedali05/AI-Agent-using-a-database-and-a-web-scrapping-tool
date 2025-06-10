-- filepath: c:\PostGress_Database\populate_bdd.sql
-- Insert beauty products
INSERT INTO Product (nom, description, ingrédients, prix) VALUES
('Crème Hydratante', 'Crème visage hydratante pour peau sèche', 'acide hyaluronique, aloé vera, vitamine E', 14.90),
('Shampooing Bio', 'Shampooing doux sans sulfates', 'huile d’argan, camomille, extraits de bambou', 9.50),
('Masque Capillaire', 'Masque réparateur pour cheveux abîmés', 'kératine, beurre de karité, huile de coco', 12.75),
('Sérum Anti-âge', 'Sérum visage régénérant', 'rétinol, peptides, acide hyaluronique', 24.30),
('Crayon à Lèvres', 'Crayon longue tenue pour les lèvres', 'cire d’abeille, pigments naturels, beurre de cacao', 6.80);

-- Insert beauty stores
INSERT INTO Store (nom, adresse) VALUES
('Beauté Naturelle', '10 Rue des Lilas'),
('Éclat Parisien', '45 Avenue Montaigne'),
('Zen Cosmétiques', '88 Boulevard Haussmann');

-- Insert stock per store
INSERT INTO Store_Products (id_store, id_product, stock_unit) VALUES
(1, 1, 50), -- Crème Hydratante
(1, 2, 30), -- Shampooing Bio
(1, 3, 20), -- Masque Capillaire

(2, 1, 40),
(2, 4, 25), -- Sérum Anti-âge
(2, 5, 60), -- Crayon à Lèvres

(3, 2, 35),
(3, 3, 15),
(3, 5, 50);