SELECT O.*
FROM Persons AS P
INNER JOIN Orders AS O ON P.Id_P = O.Id_P;
