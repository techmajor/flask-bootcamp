def row2Dict(row):
  ret = {}
  for column in row.__table__.columns:
        ret[column.name] = str(getattr(row, column.name))
  return ret