DROP TABLE IF EXISTS federation;
DROP TABLE IF EXISTS pod;

CREATE TABLE pod(
  podName VARCHAR(255)
);

CREATE TABLE federation(
  podId INT,
  pod1 VARCHAR(255),
  pod2 VARCHAR(255),
  success BOOLEAN
);
