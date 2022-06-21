from typing_extensions import Self
from search_engine.irma_code import IRMA
from search_engine.query import Query
import os

class Handler:

    def __init__(self):
        self._irma = IRMA()
        self._query = Query()
        self.query_image = ''
        self.results = []

    def query(self, image_path : str, limit = 10) -> list:
        self.results = []
        self._retrieve_results(image_path, limit)
        print(self.results, flush=True)
        self._get_irma()
        return self.results

    def _retrieve_results(self, image_path : str, limit):
        self._query.set_image_name(image_path)
        results = self._query.run(limit)
        images_path = os.path.join(*(results[0][0].split(f"{os.sep}")[0:-1]))
        for image_path, distance in results:
            print(images_path, flush=True)
            image_name = image_path.split(f"{os.sep}")[-1]
            self.results.append(f"images/{image_name}")

    def _get_irma(self) -> None:
        irma_codes = self._irma.get_irma([self._image_name(x) for x in self.results])
        print([self._image_name(x) for x in self.results], flush=True)

        tmp = []
        print(self.results, flush=True)
        print(irma_codes, flush=True)
        for image, code in zip(self.results, irma_codes):
            tmp.append((image, self._irma.decode_as_dict(code)))

        self.results = tmp

    def relevance_feedback(self, selected_images, not_selected_images) -> None:
        return self._query.relevance_feedback(selected_images, not_selected_images)

    @staticmethod
    def _image_name(image_path : str) -> str:
        return image_path.split(f"{os.sep}")[-1]
        