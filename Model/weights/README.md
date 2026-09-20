Model Weights — storage location
Trained weights are not committed to Git (file size). They will be stored inGoogle Drive and recorded here after training.

Artifact	Drive path	Size (est.)	Notes
best_model.keras	MyDrive/mangrove_project/models/	~200–350 MB	best validation checkpoint
final_model.keras	MyDrive/mangrove_project/models/	~200–350 MB	restored-best final model (locked config + threshold)
loss_curve.png	MyDrive/mangrove_project/models/	< 1 MB	train vs. validation loss (overfitting check)
After training, fill in:

Drive link: (to be added)
SHA-256 of final_model.keras: (to be added — run certutil -hashfile <file> SHA256 / shasum -a 256 <file>)
Locked operating threshold: (to be added — see Model/metrics.json)
Weights must only ever be loaded together with the locked threshold recorded inModel/metrics.json — applying the model at a different threshold is outsidethe study's validated configuration.

