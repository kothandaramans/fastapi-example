from fastapi import status, HTTPException, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(''' SELECT * FROM posts ''')
    # posts = cursor.fetchall()
    print(search)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # end comma intention not sure
    # cursor.execute(''' SELECT * FROM posts where id = %s ''', (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(''' INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ''',
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    print(current_user.id)
    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     ''' DELETE FROM posts WHERE id = %s RETURNING * ''', (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = post_query.first()

    if (deleted_post == None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
    if (deleted_post.user_id != int(current_user.id)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform the requested action"
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(''' UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * ''',
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if (updated_post == None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )

    if (updated_post.user_id != int(current_user.id)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform the requested action"
        )

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post
