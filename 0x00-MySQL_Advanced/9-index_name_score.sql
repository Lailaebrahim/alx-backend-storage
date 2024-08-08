-- Creates an index idx_name_first on the first letter of name of name table and the score.
CREATE INDEX idx_name_first_score ON names(name(1), score);
