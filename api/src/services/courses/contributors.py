from datetime import datetime
from fastapi import HTTPException, Request, status
from sqlmodel import Session, select, and_
from src.db.users import PublicUser, AnonymousUser, User, UserRead
from src.db.courses.courses import Course
from src.db.resource_authors import ResourceAuthor, ResourceAuthorshipEnum, ResourceAuthorshipStatusEnum
from src.security.rbac.rbac import authorization_verify_if_user_is_anon, authorization_verify_based_on_roles_and_authorship
from typing import List


async def apply_course_contributor(
    request: Request,
    course_uuid: str,
    current_user: PublicUser | AnonymousUser,
    db_session: Session,
):
    # Verify user is not anonymous
    await authorization_verify_if_user_is_anon(current_user.id)

    # Check if course exists
    statement = select(Course).where(Course.course_uuid == course_uuid)
    course = db_session.exec(statement).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    # Check if user already has any authorship role for this course
    existing_authorship = db_session.exec(
        select(ResourceAuthor).where(
            and_(
                ResourceAuthor.resource_uuid == course_uuid,
                ResourceAuthor.user_id == current_user.id
            )
        )
    ).first()

    if existing_authorship:
        raise HTTPException(
            status_code=400,
            detail="You already have an authorship role for this course",
        )

    # Create pending contributor application
    resource_author = ResourceAuthor(
        resource_uuid=course_uuid,
        user_id=current_user.id,
        authorship=ResourceAuthorshipEnum.CONTRIBUTOR,
        authorship_status=ResourceAuthorshipStatusEnum.PENDING,
        creation_date=str(datetime.now()),
        update_date=str(datetime.now()),
    )

    db_session.add(resource_author)
    db_session.commit()
    db_session.refresh(resource_author)

    return {
        "detail": "Contributor application submitted successfully",
        "status": "pending"
    }

async def update_course_contributor(
    request: Request,
    course_uuid: str,
    contributor_user_id: int,
    authorship: ResourceAuthorshipEnum,
    authorship_status: ResourceAuthorshipStatusEnum,
    current_user: PublicUser | AnonymousUser,
    db_session: Session,
):
    """
    Update a course contributor's role and status
    Only administrators can perform this action
    """
    # Verify user is not anonymous
    await authorization_verify_if_user_is_anon(current_user.id)

    # RBAC check - verify if user has admin rights
    authorized = await authorization_verify_based_on_roles_and_authorship(
        request, current_user.id, "update", course_uuid, db_session
    )

    if not authorized:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update course contributors",
        )

    # Check if course exists
    statement = select(Course).where(Course.course_uuid == course_uuid)
    course = db_session.exec(statement).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    # Check if the contributor exists for this course
    existing_authorship = db_session.exec(
        select(ResourceAuthor).where(
            and_(
                ResourceAuthor.resource_uuid == course_uuid,
                ResourceAuthor.user_id == contributor_user_id
            )
        )
    ).first()

    if not existing_authorship:
        raise HTTPException(
            status_code=404,
            detail="Contributor not found for this course",
        )

    # Don't allow changing the role of the creator
    if existing_authorship.authorship == ResourceAuthorshipEnum.CREATOR:
        raise HTTPException(
            status_code=400,
            detail="Cannot modify the role of the course creator",
        )

    # Update the contributor's role and status
    existing_authorship.authorship = authorship
    existing_authorship.authorship_status = authorship_status
    existing_authorship.update_date = str(datetime.now())

    db_session.add(existing_authorship)
    db_session.commit()
    db_session.refresh(existing_authorship)

    return {
        "detail": "Contributor updated successfully",
        "status": "success"
    }

async def get_course_contributors(
    request: Request,
    course_uuid: str,
    current_user: PublicUser | AnonymousUser,
    db_session: Session,
) -> List[dict]:
    """
    Get all contributors for a course with their user information
    """
    # Check if course exists
    statement = select(Course).where(Course.course_uuid == course_uuid)
    course = db_session.exec(statement).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    # Get all contributors for this course with user information
    statement = (
        select(ResourceAuthor, User)
        .join(User)  # SQLModel will automatically join on foreign key
        .where(ResourceAuthor.resource_uuid == course_uuid)
    )
    results = db_session.exec(statement).all()

    return [
        {
            "user_id": contributor.user_id,
            "authorship": contributor.authorship,
            "authorship_status": contributor.authorship_status,
            "creation_date": contributor.creation_date,
            "update_date": contributor.update_date,
            "user": UserRead.model_validate(user).model_dump()
        }
        for contributor, user in results
    ] 