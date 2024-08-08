-- Creates an index idx_name_first on the first letter of name of name table.
CREATE INDEX idx_name_first ON names(name(1));
