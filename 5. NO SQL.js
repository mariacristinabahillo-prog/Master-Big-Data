--1.Analizar con find la colección. 
db.ENTREGA.find()

--2.Contar cuántos documentos (películas) tiene cargado.
db.ENTREGA.countDocuments()

--3.Insertar una película. 
db.ENTREGA.insertOne({title:"Feliz_navidad", year:2026, cast:[], genres:"Comedy"})

--4.Borrar la película insertada en el punto anterior (en el 3).
db.ENTREGA.deleteOne({_id:ObjectId("697390405e313f49fddc7656"})


--5.Contar cuantas películas tienen actores (cast) que se llaman “and”.
db.ENTREGA.find({
  cast: "and"
}).count()


--6.Actualizar los documentos cuyo actor (cast) tenga por error el valor “and” 
--como si realmente fuera un actor. Para ello, se debe sacar únicamente ese valor
--del array cast. Por lo tanto, no se debe eliminar ni el documento (película)
--ni su array cast con el resto de actores.

var query = {}
var operacion = {$pull:{"cast":"and"}}
db.ENTREGA.updateMany(query,operacion)

--7.Contar cuantos documentos (películas) tienen el array ‘cast’ vacío.
db.ENTREGA.countDocuments({ cast: [] })


--8.Actualizar TODOS los documentos (películas) que tengan el array cast
--vacío, añadiendo un nuevo elemento dentro del array con valor Undefined.
--Cuidado! El tipo de cast debe seguir siendo un array. El array debe ser así -> ["Undefined" ].
db.ENTREGA.updateMany(
  { cast: { $size: 0 } },
  { $push: { cast: "Undefined" }} 
)
 
--9.	Contar cuantos documentos (películas) tienen el array genres vacío.
 db.ENTREGA.countDocuments({ genres: [ ] })

--10.	 Actualizar TODOS los documentos (películas) que tengan el array genres vacío, añadiendo
--un nuevo elemento dentro del array con valor Undefined. Cuidado! El tipo de genres debe seguir 
--siendo un array. El array debe ser así -> ["Undefined" ]. 
db.ENTREGA.updateMany(
   { genres: { $size: 0 } },
  { $push: { genres: "Undefined" } }) 
  

--11.Mostrar el año más reciente / actual que tenemos sobre todas las películas. 
db.ENTREGA.find(
  {},
  { year: 1, _id: 0 }
).sort({ year: -1 }).limit(1)


--12.Contar cuántas películas han salido en los últimos 20 años. Debe hacerse desde el último 
--año que se tienen registradas películas en la colección, no desde la fecha actual, mostrando
--el resultado total de esos años, no el resultado por año. Revisar que no se cuentan 21 años. 
--Se debe hacer con el Framework de Agregación.

var query1= {year: { $gte: 1999 }}
var fase1 = {$match: query1}
var fase2= {$count: "Ultimos 20 años"}
var etapas=[fase1, fase2]
db.ENTREGA.aggregate(etapas)


--13.Contar cuántas películas han salido en la década de los 60 (del 60 al 69 incluidos). 
--Se debe hacer con el Framework de Agregación.

var query1 = {year: {$gte:1960, $lte: 1969}}
var fase1 = {$match:query1}
var fase2 ={$count: "Años 60"}
var etapas=[fase1,fase2]
db.ENTREGA.aggregate(etapas)

● 14. Mostrar el año u años con más películas mostrando el número de películas de ese año. Revisar si varios años
pueden compartir tener el mayor número de películas.

var query1 = { $group: { _id: "$year", total: { $sum: 1 } } }
var query2 = { $sort: { total: -1 } }
var query3 = { $limit: 1 }
var etapas = [query1,query2,query3]
db.ENTREGA.aggregate(etapas)


● 15. Mostrar el año u años con menos películas mostrando el número de películas de ese año. Revisar si varios años
pueden compartir tener el menor número de películas. 
var query1 = { $group: { _id: "$year", total: { $sum: 1 } } }
var query2 = { $sort: { total: 1 } }
var query3 = { $limit: 3 }
var etapas = [query1,query2,query3]
db.ENTREGA.aggregate(etapas)



16. Guardar en nueva colección llamada “actors” realizando la fase $unwind por cast, no se debe agrupar de nuevo y
debe contener todas las claves (title,year,cast,genres). Después, contar cuantos documentos existen en la nueva
colección. 

var query1 = { $match: {cast: { $exists: true, $not: { $size: 0 }}}}
var query2 = { $unwind: "$cast" }
var query3 = { $project: { 
    _id: 0,       
    title: 1,
    year: 1,
    cast: 1,
    genres: 1
  }}
var query4 = { $merge: "actors" }
var etapas = [ query1,query2,query3,query4]
db.ENTREGA.aggregate(etapas)

db.actors.countDocuments()


17. Sobre actors (nueva colección), mostrar la lista con los 5 actores que han participado en más películas mostrando el
número de películas en las que ha participado. Importante! Se necesita previamente filtrar para descartar aquellos
actores llamados "Undefined". Aclarar que no se eliminan de la colección, sólo que filtramos para que no aparezcan. 

var query1 = {$match: {cast: {$ne:"Undefined"}}}
var query2 = {$group: {_id:"$cast", totalMovies: {$sum:1}}}
var query3 = {$sort: {totalMovies: -1 }}
var query4 = { $limit: 5 }
var etapas= [query1,query2,query3,query4]
db.actors.aggregate(etapas)



18. Sobre actors (nueva colección), agrupar por película y año mostrando las 5 en las que más actores hayan
participado, mostrando el número total de actores.

var query1= {$group:{ _id:{title:"$title",year:"$year"}, totalActors: {$sum:1}}}
var query2= {$sort: {totalActors: -1 }}
var query3= { $limit: 5 }
var etapas= [query1,query2,query3]
db.actors.aggregate(etapas)

19. Sobre actors (nueva colección), mostrar los 5 actores cuya carrera haya sido la más larga. Para ello, se debe
mostrar cuándo comenzó su carrera, cuándo finalizó y cuántos años ha trabajado. Importante! Se necesita previamente
filtrar para descartar aquellos actores llamados "Undefined". Aclarar que no se eliminan de la colección, sólo que
filtramos para que no aparezcan. 

var query1= {$match: {
    cast: {$ne:"Undefined"},
    year: { $ne: null }}}
var query2= { $group: { 
      _id: "$cast", 
      startYear: { $min: "$year" }, 
      endYear: { $max: "$year" }}}
var query3={ $project: { 
      actor: "$_id",
      startYear: 1,
      endYear: 1,
      Años_carrera: { $add: [ { $subtract: ["$endYear", "$startYear"] }, 1 ] }, 
      _id: 0}}
var query4=  { $sort: {Años_carrera: -1 } }
var query5= {$limit:6}
var etapas= [query1,query2,query3,query4, query5]
db.actors.aggregate(etapas)


20. Sobre actors (nueva colección), Guardar en nueva colección llamada “genres” realizando la fase $unwind por
genres, no se debe agrupar de nuevo y debe contener todas las claves (title,year,cast,genres). Después, contar cuantos
documentos existen en la nueva colección. 

var query1 = { $match: {genres: { $exists: true, $not: { $size: 0 }}}}
var query2 = { $unwind: "$genres" }
var query3 = { $project: { 
    _id: 0,       
    title: 1,
    year: 1,
    cast: 1,
    genres: 1
  }}
var query4 = { $merge: "genres"}
var etapas = [query1, query2, query3,query4]
db.actors.aggregate(etapas)

db.genres.countDocuments()

21. Sobre genres (nueva colección), mostrar los 5 documentos agrupados por “Año y Género” que más número de
películas diferentes tienen mostrando el número total de películas. Importante! Se necesita previamente filtrar para
descartar aquellos genres llamados "Undefined". Aclarar que no se eliminan de la colección, sólo que filtramos para
que no aparezcan.

var query1= {$match: {
    genres: {$ne:"Undefined"}}}
var query2= {$group:{ _id:{Genre:"$genres",year:"$year"}, totalPeliculas: {$sum:1}}}
var query3= {$sort: {totalPeliculas: -1 }}
var query4= { $limit: 5 }
var etapas = [query1, query2, query3, query4]
db.genres.aggregate(etapas)

22. Sobre genres (nueva colección), mostrar los 5 actores y los géneros en los que han participado con más número de
géneros diferentes, se debe mostrar tanto el número de géneros diferentes que ha interpretado como los diferentes
géneros además del nombre del actor. Importante! Se necesita previamente filtrar para descartar aquellos actores
llamados "Undefined". Aclarar que no se eliminan de la colección, sólo que filtramos para que no aparezcan.

query1 = {$match:
      {cast: {$ne: "Undefined" }}}
query2 = {$project: {
    _id:0,
    cast: 1,
    genres: 1}}
query3 = {$group:{ _id:"$cast", 
    generos_diferentes: { $addToSet: "$genres" }}}
query4 = {$project: {
    actor: "$_id",
    generos_diferentes: 1,
    total_generos: { $size: "$generos_diferentes" },
    _id: 0}}
var query5 = {$sort: {total_generos: -1 }}
var query6 = {$limit: 11}
db.genres.aggregate([query1,query2,query3,query4,query5,query6])


23. Sobre genres (nueva colección), mostrar las 5 películas y su año correspondiente en los que más géneros diferentes
han sido catalogados, mostrando esos géneros y el número de géneros que contiene. Importante! Se necesita
previamente filtrar para descartar aquellos genres llamados "Undefined". Aclarar que no se eliminan de la colección,
sólo que filtramos para que no aparezcan.

query1 = {$match: {
      genres: {$ne: "Undefined" }}}
var query2 = {
  $group: {
    _id: { title: "$title", year: "$year" },
    generos_diferentes: { $addToSet: "$genres" }}}
var query3 = {
  $project: {
    title: "$_id.title",
    year: "$_id.year",
    generos: "$generos_diferentes",
    total_generos: { $size: "$generos_diferentes" },
    _id: 0}}
var query4 = {$sort: {total_generos: -1 }}
var query5 = {$limit: 5}
db.genres.aggregate([query1,query2,query3,query4,query5])


24. Query libre sobre el pipeline de agregación.

/// Géneros más frecuentes en todas las películas
/// Se cuenta cuántas veces aparece cada género en la colección “genres”
var query1 = { $group: { 
    _id: "$genres", 
    totalPeliculas: { $sum: 1 }}}
var query2 = { $sort: { totalPeliculas: -1 } }
var query3 = { $limit: 5 }
db.genres.aggregate([query1,query2,query3])



25. Query libre sobre el pipeline de agregación.
//“La diferencia entre el número de documentos y el resultado del primer $group 
//indica la existencia de duplicados lógicos (mismo genero y año).” Generos distintos por año
var query1 = {$group: {_id: { year: "$year", genre: "$genres" }}}
var query2 = {$group: {_id: "$_id.year",
    totalGeneros: { $sum: 1 } }}
var query3 = {$sort: { totalGeneros: -1 }}
var query4 = {$limit: 5}
db.genres.aggregate([query1, query2, query3],query4])


26. Query libre sobre el pipeline de agregación
/// Género más frecuente del año 2000
var query1 = { $match: { year: 2000 } }
var query2 = {  $group: { _id: "$genres", 
    totalPeliculas: { $sum: 1 }}}
var query3 = { $sort: { totalPeliculas: -1 } }
var query4 = { $limit: 1 }

db.genres.aggregate([query1,query2,query3,query4])



