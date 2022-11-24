from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import os

def callbacks(lr, num_train, reduce_patience=15, stop_patience=200, model_name='best_model_'):
    checkpoint = ModelCheckpoint(
        os.path.join(PATH_TEMP_MODEL, model_name + str(num_train) + '.hdf5'), 
        monitor='val_f1', 
        verbose=1, 
        mode='max', 
        save_best_only=True
    )

    earlystop = EarlyStopping(
        monitor='val_f1', 
        mode='max', 
        patience=stop_patience, 
        restore_best_weights=True
    )

    reduce_lr = ReduceLROnPlateau(
        monitor='val_f1', 
        mode='max', 
        factor=0.9, 
        patience=reduce_patience, # можно 10
        verbose=1, 
        min_lr=lr/10000
    )
    
    return [checkpoint, earlystop, reduce_lr]