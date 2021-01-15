from __future__ import print_function
import os, binascii, sys
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint # import render_template function for rendering HTML pages individually, url 4 for finding files in the background
from flask_login import current_user, login_required
from imgRepFlask import db, bcrypt, constants
from imgRepFlask.models import Album, Picture                          # Using models in views, DB needs to exist first
from imgRepFlask.images.forms import UploadPhotoForm
from imgRepFlask.users.utils import save_image

images = Blueprint('images', __name__)

@images.route('/browse')
@login_required
def browse_page():
    images = list()
    page = request.args.get('page', 1, type=int) # will throw error if not int
    albums = Album.query.order_by(Album.date.desc()).filter_by(user_id=current_user.id).paginate(page=page, per_page=5)
    print(albums, sep='\n', file=sys.stderr)
    if not albums:
        flash('There are currently no albums to view, add an album first!', 'danger')
        return redirect(url_for('main.home_page'))
    else:
        for album in albums.items:
            photos = Picture.query.filter_by(album_id=album.id).first()
            images.append(photos)
            print(images, sep='\n', file=sys.stderr)
        return render_template('browse.html', title='Browse Photos', photos = images, albums = albums)

@images.route('/upload', methods=['GET', 'POST'])
@login_required         
def upload_image():
    form = UploadPhotoForm()
    if form.validate_on_submit():
        album = Album(name = form.name.data, user_id=current_user.id)
        db.session.add(album)
        for file in form.image_file.data:
            image = Picture(name = form.name.data, image_file = save_image(file), poster=album)
            db.session.add(image)
        db.session.commit()
        flash('Photos have been uploaded!', 'success')
        return redirect(url_for('images.upload_image'))
    return render_template('upload.html', title='Upload Photos', form=form)

@images.route('/album/<int:album_id>')
@login_required         
def album(album_id):
    photos = Picture.query.filter_by(album_id=album_id).all()
    return render_template('album.html', title="Browse Album", photos = photos)

# Delete all photos first, then album
@images.route("/album/<int:album_id>/delete", methods=['GET'])
@login_required
def delete_album(album_id):
    album = Album.query.get_or_404(album_id)
    if album.user_id != current_user.id:
        abort(403)
    photos = Picture.query.filter_by(album_id=album_id).all()
    for photo in photos:
        db.session.delete(photo)
    print(album, sep='\n', file=sys.stderr)
    db.session.delete(album)
    db.session.commit()
    flash('Album has been deleted!', 'success')
    return redirect(url_for('main.home_page'))

# Delete photo, echk if album is empty, if so, delete album/
@images.route("/album/<int:album_id>/<int:picture_id>/delete", methods=['GET'])
@login_required
def delete_picture(album_id, picture_id):
    album = Album.query.get_or_404(album_id)                                # Get album object                            # Grab selected photo                                              # Store album id
    if album.user_id != current_user.id:                                    # Check if user is allowed to access
        abort(403)
    photo = Picture.query.get_or_404(picture_id)
    album_id = photo.album_id 
    db.session.delete(photo)                                                # Delete
    last_photo_check = Picture.query.filter_by(album_id=album_id).all()     # Check if photos exist with album id
    if not last_photo_check:
        db.session.delete(album)                                            # Delete album
    db.session.commit() 
    flash('Photo has been deleted!', 'success')
    return redirect(url_for('images.browse_page'))