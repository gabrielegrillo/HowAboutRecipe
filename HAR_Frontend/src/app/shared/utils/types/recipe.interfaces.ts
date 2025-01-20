
// Interfaces for Recipes & Correlated Objects

// Recipe
export interface RecipeInterface {
    "id": string,
    
    "title": string,
    "description": string,
    "created_at"?: string,
    
    "preparation_time": number,
    "difficulty": number,
    
    "steps": string,
    
    "is_public": boolean,
    "approved": boolean,

    "tags": TagInterface[],
    "ingredients": IngredientInterface[],
    "image": ImageInterface,

    "ratings": number,
    "average_rating": number

}

// Tag
export interface TagInterface {
    "id": string,
    "name": string,
}

// Ingredient & Ingredient Description
export interface IngredientDescriptionInterface {
    "id": string,
    "name": string,
}
export interface IngredientInterface {
    "ingredient": IngredientDescriptionInterface,
    "quantity": number,
    "unit": string
}

// Image & Image Description
export interface ImageInterface {
    "id": string,
    "description": string,
}
