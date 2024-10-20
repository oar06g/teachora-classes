import connect from "../config/db.js"

export async function addCourse(req, res) {
  const title = req.query.title;
  const description = req.query.description;
  const price = req.query.price;
  const material = req.query.material;

  // if (!title || description || price || material) {

  // }
}