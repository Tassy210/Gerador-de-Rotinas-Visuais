BEGIN;
--
-- Create model Categoria
--
CREATE TABLE "rotinas_categoria" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nome" varchar(50) NOT NULL, "pictograma_padrao" varchar(255) NULL, "pictograma_upload" varchar(100) NULL, "usuario_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Rotina
--
CREATE TABLE "rotinas_rotina" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "titulo" varchar(100) NOT NULL, "descricao" text NULL, "categoria_id" bigint NULL REFERENCES "rotinas_categoria" ("id") DEFERRABLE INITIALLY DEFERRED, "usuario_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Atividade
--
CREATE TABLE "rotinas_atividade" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "titulo" varchar(100) NOT NULL, "descricao" text NULL, "pictograma" varchar(100) NULL, "pictograma_padrao" varchar(255) NULL, "ordem" integer unsigned NOT NULL CHECK ("ordem" >= 0), "usuario_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "rotina_id" bigint NOT NULL REFERENCES "rotinas_rotina" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create constraint unique_categoria_por_usuario on model categoria
--
CREATE TABLE "new__rotinas_categoria" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nome" varchar(50) NOT NULL, "pictograma_padrao" varchar(255) NULL, "pictograma_upload" varchar(100) NULL, "usuario_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, CONSTRAINT "unique_categoria_por_usuario" UNIQUE ("nome", "usuario_id"));
INSERT INTO "new__rotinas_categoria" ("id", "nome", "pictograma_padrao", "pictograma_upload", "usuario_id") SELECT "id", "nome", "pictograma_padrao", "pictograma_upload", "usuario_id" FROM "rotinas_categoria";
DROP TABLE "rotinas_categoria";
ALTER TABLE "new__rotinas_categoria" RENAME TO "rotinas_categoria";
CREATE INDEX "rotinas_rotina_categoria_id_4f6e308c" ON "rotinas_rotina" ("categoria_id");
CREATE INDEX "rotinas_rotina_usuario_id_b901d94c" ON "rotinas_rotina" ("usuario_id");
CREATE INDEX "rotinas_atividade_usuario_id_5fa24599" ON "rotinas_atividade" ("usuario_id");
CREATE INDEX "rotinas_atividade_rotina_id_fbbd968f" ON "rotinas_atividade" ("rotina_id");
CREATE INDEX "rotinas_categoria_usuario_id_9685bf6d" ON "rotinas_categoria" ("usuario_id");
COMMIT;
